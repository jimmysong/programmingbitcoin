from io import BytesIO
from unittest import TestCase

from block import GENESIS_BLOCK_HASH
from helper import (
    calculate_new_bits,
    encode_varint,
    hash256,
    int_to_little_endian,
    little_endian_to_int,
)
from network import (
    GetHeadersMessage,
    HeadersMessage,
    NetworkEnvelope,
    SimpleNode,
    VersionMessage,
    NETWORK_MAGIC,
    TESTNET_NETWORK_MAGIC,
)


class Chapter10Test(TestCase):

    def test_apply(self):

        @classmethod
        def parse(cls, s, testnet=False):
            magic = s.read(4)
            if magic == b'':
                raise IOError('Connection reset!')
            if testnet:
                expected_magic = TESTNET_NETWORK_MAGIC
            else:
                expected_magic = NETWORK_MAGIC
            if magic != expected_magic:
                raise SyntaxError('magic is not right {} vs {}'.format(magic.hex(), expected_magic.hex()))
            command = s.read(12)
            command = command.strip(b'\x00')
            payload_length = little_endian_to_int(s.read(4))
            checksum = s.read(4)
            payload = s.read(payload_length)
            calculated_checksum = hash256(payload)[:4]
            if calculated_checksum != checksum:
                raise IOError('checksum does not match')
            return cls(command, payload, testnet=testnet)

        def serialize(self):
            result = self.magic
            result += self.command + b'\x00' * (12 - len(self.command))
            result += int_to_little_endian(len(self.payload), 4)
            result += hash256(self.payload)[:4]
            result += self.payload
            return result

        def serialize_2(self):
            result = int_to_little_endian(self.version, 4)
            result += int_to_little_endian(self.services, 8)
            result += int_to_little_endian(self.timestamp, 8)
            result += int_to_little_endian(self.receiver_services, 8)
            result += b'\x00' * 10 + b'\xff\xff' + self.receiver_ip
            result += int_to_little_endian(self.receiver_port, 2)
            result += int_to_little_endian(self.sender_services, 8)
            result += b'\x00' * 10 + b'\xff\xff' + self.sender_ip
            result += int_to_little_endian(self.sender_port, 2)
            result += self.nonce
            result += encode_varint(len(self.user_agent))
            result += self.user_agent
            result += int_to_little_endian(self.latest_block, 4)
            if self.relay:
                result += b'\x01'
            else:
                result += b'\x00'
            return result

        def handshake(self):
            version = VersionMessage()
            self.send(version.command, version.serialize())
            self.wait_for_commands({b'verack'})

        def serialize_3(self):
            result = int_to_little_endian(self.version, 4)
            result += encode_varint(self.num_hashes)
            result += self.start_block[::-1]
            result += self.end_block[::-1]
            return result

        NetworkEnvelope.parse = parse
        NetworkEnvelope.serialize = serialize
        VersionMessage.serialize = serialize_2
        SimpleNode.handshake = handshake
        GetHeadersMessage.serialize = serialize_3

    def test_exercise_1(self):
        message_hex = 'f9beb4d976657261636b000000000000000000005df6e0e2'
        stream = BytesIO(bytes.fromhex(message_hex))
        envelope = NetworkEnvelope.parse(stream)
        self.assertEqual(envelope.command, b'verack')
        self.assertEqual(envelope.payload, b'')

    def test_example_1(self):
        node = SimpleNode('btc.programmingblockchain.com', testnet=False)
        node.handshake()
        last_block_hash = GENESIS_BLOCK_HASH
        first_epoch_block = None
        expected_bits = None
        count = 1
        want = ('ffff001d', 'ffff001d', 'ffff001d', 'ffff001d', 'ffff001d', 'ffff001d', 'ffff001d', 'ffff001d', 'ffff001d', 'ffff001d', 'ffff001d', 'ffff001d', 'ffff001d', 'ffff001d', 'ffff001d', 'ffff001d', '6ad8001d', '28c4001d')
        for bits in want:
            getheaders = GetHeadersMessage(start_block=last_block_hash)
            node.send(getheaders.command, getheaders.serialize())
            headers_envelope = node.wait_for_commands([b'headers'])
            headers_message = HeadersMessage.parse(headers_envelope.stream())
            for block in headers_message.blocks:
                if not block.check_pow():
                    raise RuntimeError('bad proof of work at block {}'.format(count))
                if last_block_hash != GENESIS_BLOCK_HASH and block.prev_block != last_block_hash:
                    raise RuntimeError('discontinuous block at {}'.format(count))
                if expected_bits and block.bits != expected_bits:
                    raise RuntimeError('bad bits at block {} {} vs {}'.format(count, block.bits.hex(), expected_bits.hex()))
                if first_epoch_block and count % 2016 == 2015:
                    expected_bits = calculate_new_bits(
                        expected_bits, block.timestamp - first_epoch_block.timestamp)
                    self.assertEqual(expected_bits.hex(), bits)
                elif first_epoch_block is None:
                    expected_bits = block.bits
                if count % 2016 == 0 or not first_epoch_block:
                    first_epoch_block = block
                count += 1
                last_block_hash = block.hash()
