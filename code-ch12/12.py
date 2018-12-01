from unittest import TestCase

from bloomfilter import BloomFilter, BIP37_CONSTANT
from ecc import PrivateKey
from helper import (
    bit_field_to_bytes,
    decode_base58,
    encode_varint,
    hash160,
    hash256,
    int_to_little_endian,
    little_endian_to_int,
    murmur3,
)
from merkleblock import MerkleBlock
from network import (
    GenericMessage,
    GetDataMessage,
    GetHeadersMessage,
    HeadersMessage,
    SimpleNode,
    FILTERED_BLOCK_DATA_TYPE,
)
from script import p2pkh_script, Script
from tx import Tx, TxIn, TxOut, TxFetcher


def add(self, item):
    for i in range(self.function_count):
        seed = i * BIP37_CONSTANT + self.tweak
        h = murmur3(item, seed=seed)
        bit = h % (self.size * 8)
        self.bit_field[bit] = 1

        
def filterload(self, flag=1):
    payload = encode_varint(self.size)
    payload += self.filter_bytes()
    payload += int_to_little_endian(self.function_count, 4)
    payload += int_to_little_endian(self.tweak, 4)
    payload += int_to_little_endian(flag, 1)
    return GenericMessage(b'filterload', payload)


def serialize(self):
    result = encode_varint(len(self.data))
    for data_type, identifier in self.data:
        result += int_to_little_endian(data_type, 4)
        result += identifier[::-1]
    return result


class Chapter12Test(TestCase):

    def test_apply(self):
        BloomFilter.add = add
        BloomFilter.filterload = filterload
        GetDataMessage.serialize = serialize

    def test_example_1(self):
        bit_field_size = 10
        bit_field = [0] * bit_field_size
        h = hash256(b'hello world')
        bit = int.from_bytes(h, 'big') % bit_field_size
        bit_field[bit] = 1
        self.assertEqual(bit_field, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1])

    def test_example_2(self):
        bit_field_size = 10
        bit_field = [0] * bit_field_size
        for item in (b'hello world', b'goodbye'):
            h = hash256(item)
            bit = int.from_bytes(h, 'big') % bit_field_size
            bit_field[bit] = 1
        self.assertEqual(bit_field, [0, 0, 1, 0, 0, 0, 0, 0, 0, 1])

    def test_exercise_1(self):
        bit_field_size = 10
        bit_field = [0] * bit_field_size
        for item in (b'hello world', b'goodbye'):
            h = hash160(item)
            bit = int.from_bytes(h, 'big') % bit_field_size
            bit_field[bit] = 1
        self.assertEqual(bit_field, [1, 1, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_example_3(self):
        bit_field_size = 10
        bit_field = [0] * bit_field_size
        for item in (b'hello world', b'goodbye'):
            for hash_function in (hash256, hash160):
                h = hash_function(item)
                bit = int.from_bytes(h, 'big') % bit_field_size
                bit_field[bit] = 1
        self.assertEqual(bit_field, [1, 1, 1, 0, 0, 0, 0, 0, 0, 1])

    def test_example_4(self):
        field_size = 2
        num_functions = 2
        tweak = 42
        bit_field_size = field_size * 8
        bit_field = [0] * bit_field_size
        for phrase in (b'hello world', b'goodbye'):
            for i in range(num_functions):
                seed = i * BIP37_CONSTANT + tweak
                h = murmur3(phrase, seed=seed)
                bit = h % bit_field_size
                bit_field[bit] = 1
        self.assertEqual(bit_field, [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0])

    def test_exercise_2(self):
        field_size = 10
        function_count = 5
        tweak = 99
        items = (b'Hello World', b'Goodbye!')
        bit_field_size = field_size * 8
        bit_field = [0] * bit_field_size
        for item in items:
            for i in range(function_count):
                seed = i * BIP37_CONSTANT + tweak
                h = murmur3(item, seed=seed)
                bit = h % bit_field_size
                bit_field[bit] = 1
        self.assertEqual(bit_field_to_bytes(bit_field).hex(), '4000600a080000010940')

    def test_example_5(self):
        last_block_hex = '00000000000538d5c2246336644f9a4956551afb44ba47278759ec55ea912e19'
        address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'
        h160 = decode_base58(address)
        node = SimpleNode('tbtc.programmingblockchain.com', testnet=True, logging=False)
        bf = BloomFilter(30, 5, 90210)
        bf.add(h160)
        node.handshake()
        node.send(bf.filterload())
        start_block = bytes.fromhex(last_block_hex)
        getheaders = GetHeadersMessage(start_block=start_block)
        node.send(getheaders)
        headers = node.wait_for(HeadersMessage)
        getdata = GetDataMessage()
        for b in headers.blocks:
            if not b.check_pow():
                raise RuntimeError('proof of work is invalid')
            getdata.add_data(FILTERED_BLOCK_DATA_TYPE, b.hash())
        node.send(getdata)
        found = False
        while not found:
            message = node.wait_for(MerkleBlock, Tx)
            if message.command == b'merkleblock':
                if not message.is_valid():
                    raise RuntimeError('invalid merkle proof')
            else:
                for i, tx_out in enumerate(message.tx_outs):
                    if tx_out.script_pubkey.address(testnet=True) == address:
                        self.assertEqual(
                            message.id(),
                            'e3930e1e566ca9b75d53b0eb9acb7607f547e1182d1d22bd4b661cfe18dcddf1')
                        self.assertEqual(i, 0)
                        found = True
                        break

    def test_exercise_6(self):
        last_block_hex = '000000000d65610b5af03d73ed67704713c9b734d87cf4b970d39a0416dd80f9'
        secret = little_endian_to_int(hash256(b'Jimmy Song Programming Blockchain'))
        private_key = PrivateKey(secret=secret)
        addr = private_key.point.address(testnet=True)
        h160 = decode_base58(addr)
        target_address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'
        self.assertEqual(addr, target_address)
        target_h160 = decode_base58(target_address)
        target_script = p2pkh_script(target_h160)
        fee = 5000
        node = SimpleNode('tbtc.programmingblockchain.com', testnet=True)
        bf = BloomFilter(30, 5, 90210)
        bf.add(h160)
        node.handshake()
        node.send(bf.filterload())
        start_block = bytes.fromhex(last_block_hex)
        getheaders = GetHeadersMessage(start_block=start_block)
        node.send(getheaders)
        headers = node.wait_for(HeadersMessage)
        last_block = None
        getdata = GetDataMessage()
        for b in headers.blocks:
            if not b.check_pow():
                raise RuntimeError('proof of work is invalid')
            if last_block is not None and b.prev_block != last_block:
                raise RuntimeError('chain broken')
            getdata.add_data(FILTERED_BLOCK_DATA_TYPE, b.hash())
            last_block = b.hash()
        node.send(getdata)
        prev_tx, prev_index = None, None
        while prev_tx is None:
            message = node.wait_for(MerkleBlock, Tx)
            if message.command == b'merkleblock':
                if not message.is_valid():
                    raise RuntimeError('invalid merkle proof')
            else:
                message.testnet = True
                for i, tx_out in enumerate(message.tx_outs):
                    if tx_out.script_pubkey.address(testnet=True) == addr:
                        prev_tx = message.hash()
                        prev_index = i
                        prev_amount = tx_out.amount
                        self.assertEqual(
                            message.id(),
                            '6ec96c9eafc62c0e42a4a6965be614c61101aaa316162ac79e07e1b9ab31e694')
                        self.assertEqual(i, 0)
                        break
        tx_in = TxIn(prev_tx, prev_index)
        output_amount = prev_amount - fee
        tx_out = TxOut(output_amount, target_script)
        tx_obj = Tx(1, [tx_in], [tx_out], 0, testnet=True)
        tx_obj.sign_input(0, private_key)
        self.assertEqual(tx_obj.serialize().hex(), '010000000194e631abb9e1079ec72a1616a3aa0111c614e65b96a6a4420e2cc6af9e6cc96e000000006a47304402203cc8c56abe1c0dd043afa9eb125dafbebdde2dd4cd7abf0fb1aae0667a22006e02203c95b74d0f0735bbf1b261d36e077515b6939fc088b9d7c1b7030a5e494596330121021cdd761c7eb1c90c0af0a5963e94bf0203176b4662778d32bd6d7ab5d8628b32ffffffff01f8829800000000001976a914ad346f8eb57dee9a37981716e498120ae80e44f788ac00000000')
