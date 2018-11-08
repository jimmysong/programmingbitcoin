from io import BytesIO
from unittest import TestCase

import helper

from block import Block
from helper import (
    hash256,
    int_to_little_endian,
    little_endian_to_int,
    target_to_bits,
    TWO_WEEKS,
)
from script import Script
from tx import Tx

class Chapter9Test(TestCase):

    def test_apply(self):
        
        def is_coinbase(self):
            if len(self.tx_ins) != 1:
                return False
            first_input = self.tx_ins[0]
            if first_input.prev_tx != b'\x00' * 32:
                return False
            if first_input.prev_index != 0xffffffff:
                return False
            return True

        def coinbase_height(self):
            if not self.is_coinbase():
                return None
            element = self.tx_ins[0].script_sig.instructions[0]
            return little_endian_to_int(element)

        @classmethod
        def parse(cls, s):
            version = little_endian_to_int(s.read(4))
            prev_block = s.read(32)[::-1]
            merkle_root = s.read(32)[::-1]
            timestamp = little_endian_to_int(s.read(4))
            bits = s.read(4)
            nonce = s.read(4)
            return cls(version, prev_block, merkle_root, timestamp, bits, nonce)

        def serialize(self):
            result = int_to_little_endian(self.version, 4)
            result += self.prev_block[::-1]
            result += self.merkle_root[::-1]
            result += int_to_little_endian(self.timestamp, 4)
            result += self.bits
            result += self.nonce
            return result

        def hash(self):
            s = self.serialize()
            sha = hash256(s)
            return sha[::-1]

        def bip9(self):
            return self.version >> 29 == 0b001

        def bip91(self):
            return self.version >> 4 & 1 == 1

        def bip141(self):
            return self.version >> 1 & 1 == 1

        def bits_to_target(bits):
            exponent = bits[-1]
            coefficient = little_endian_to_int(bits[:-1])
            return coefficient * 256**(exponent - 3)

        def target(self):
            return bits_to_target(self.bits)
        
        def difficulty(self):
            lowest = 0xffff * 256**(0x1d - 3)
            return lowest / self.target()

        def check_pow(self):
            sha = hash256(self.serialize())
            proof = little_endian_to_int(sha)
            return proof < self.target()

        def calculate_new_bits(previous_bits, time_differential):
            if time_differential > TWO_WEEKS * 4:
                time_differential = TWO_WEEKS * 4
            if time_differential < TWO_WEEKS // 4:
                time_differential = TWO_WEEKS // 4
            new_target = bits_to_target(previous_bits) * time_differential // TWO_WEEKS
            return target_to_bits(new_target)

        Tx.is_coinbase = is_coinbase
        Tx.coinbase_height = coinbase_height
        Block.parse = parse
        Block.serialize = serialize
        Block.hash = hash
        Block.bip9 = bip9
        Block.bip91 = bip91
        Block.bip141 = bip141
        Block.target = target
        Block.difficulty = difficulty
        Block.check_pow = check_pow
        helper.calculate_new_bits = calculate_new_bits

    def test_example_1(self):
        stream = BytesIO(bytes.fromhex('4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73'))
        s = Script.parse(stream)
        self.assertEqual(s.instructions[2], b'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks')

    def test_example_2(self):
        stream = BytesIO(bytes.fromhex('5e03d71b07254d696e656420627920416e74506f6f6c20626a31312f4542312f4144362f43205914293101fabe6d6d678e2c8c34afc36896e7d9402824ed38e856676ee94bfdb0c6c4bcd8b2e5666a0400000000000000c7270000a5e00e00'))
        script_sig = Script.parse(stream)
        self.assertEqual(little_endian_to_int(script_sig.instructions[0]), 465879)

    def test_example_3(self):
        block_id = hash256(bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d'))
        self.assertEqual(block_id.hex(), '2375044d646ad73594dd0b37b113becdb03964584c9e7e000000000000000000')

    def test_example_4(self):
        b = Block.parse(BytesIO(bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d')))
        self.assertTrue(b.version >> 29 == 0b001)
        self.assertFalse(b.version >> 4 & 1 == 1)
        self.assertTrue(b.version >> 1 & 1 == 1)

    def test_example_5(self):
        block_id = hash256(bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d'))[::-1]
        self.assertEqual('{}'.format(block_id.hex()).zfill(64), '0000000000000000007e9e4c586439b0cdbe13b1370bdd9435d76a644d047523')

    def test_example_6(self):
        bits = bytes.fromhex('e93c0118')
        exponent = bits[-1]
        coefficient = little_endian_to_int(bits[:-1])
        target = coefficient*256**(exponent-3)
        self.assertEqual('{:x}'.format(target).zfill(64), '0000000000000000013ce9000000000000000000000000000000000000000000')

    def test_example_7(self):
        bits = bytes.fromhex('e93c0118')
        exponent = bits[-1]
        coefficient = little_endian_to_int(bits[:-1])
        target = coefficient*256**(exponent-3)
        proof = little_endian_to_int(hash256(bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d')))
        self.assertTrue(proof < target)

    def test_example_8(self):
        bits = bytes.fromhex('e93c0118')
        exponent = bits[-1]
        coefficient = little_endian_to_int(bits[:-1])
        target = coefficient*256**(exponent-3)
        difficulty = 0xffff * 256**(0x1d-3) // target
        self.assertEqual(difficulty, 888171856257)

    def test_example_9(self):
        last_block = Block.parse(BytesIO(bytes.fromhex('00000020fdf740b0e49cf75bb3d5168fb3586f7613dcc5cd89675b0100000000000000002e37b144c0baced07eb7e7b64da916cd3121f2427005551aeb0ec6a6402ac7d7f0e4235954d801187f5da9f5')))
        first_block = Block.parse(BytesIO(bytes.fromhex('000000201ecd89664fd205a37566e694269ed76e425803003628ab010000000000000000bfcade29d080d9aae8fd461254b041805ae442749f2a40100440fc0e3d5868e55019345954d80118a1721b2e')))
        time_differential = last_block.timestamp - first_block.timestamp
        if time_differential > TWO_WEEKS * 4:
            time_differential = TWO_WEEKS * 4
        if time_differential < TWO_WEEKS // 4:
            time_differential = TWO_WEEKS // 4
        new_target = last_block.target() * time_differential // TWO_WEEKS
        self.assertEqual('{:x}'.format(new_target).zfill(64), '0000000000000000007615000000000000000000000000000000000000000000')

    def test_exercise_8(self):
        block1_hex = '000000203471101bbda3fe307664b3283a9ef0e97d9a38a7eacd8800000000000000000010c8aba8479bbaa5e0848152fd3c2289ca50e1c3e58c9a4faaafbdf5803c5448ddb845597e8b0118e43a81d3'
        block2_hex = '02000020f1472d9db4b563c35f97c428ac903f23b7fc055d1cfc26000000000000000000b3f449fcbe1bc4cfbcb8283a0d2c037f961a3fdf2b8bedc144973735eea707e1264258597e8b0118e5f00474'
        last_block = Block.parse(BytesIO(bytes.fromhex(block1_hex)))
        first_block = Block.parse(BytesIO(bytes.fromhex(block2_hex)))
        time_differential = last_block.timestamp - first_block.timestamp
        if time_differential > TWO_WEEKS * 4:
            time_differential = TWO_WEEKS * 4
        if time_differential < TWO_WEEKS // 4:
            time_differential = TWO_WEEKS // 4
        new_target = last_block.target() * time_differential // TWO_WEEKS
        new_bits = target_to_bits(new_target)
        self.assertEqual(new_bits.hex(),'80df6217')
