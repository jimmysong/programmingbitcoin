from io import BytesIO
from unittest import TestCase

import helper
import op

from ecc import S256Point, Signature
from helper import (
    encode_base58_checksum,
    encode_varint,
    hash256,
    int_to_little_endian,
)
from op import decode_num, encode_num
from script import Script
from tx import Tx, TxIn, SIGHASH_ALL


class Chapter8Test(TestCase):

    def test_apply(self):
        
        def op_checkmultisig(stack, z):
            if len(stack) < 1:
                return False
            n = decode_num(stack.pop())
            if len(stack) < n + 1:
                return False
            sec_pubkeys = []
            for _ in range(n):
                sec_pubkeys.append(stack.pop())
            m = decode_num(stack.pop())
            if len(stack) < m + 1:
                return False
            der_signatures = []
            for _ in range(m):
                der_signatures.append(stack.pop()[:-1])
            stack.pop()
            try:
                points = [S256Point.parse(sec) for sec in sec_pubkeys]
                sigs = [Signature.parse(der) for der in der_signatures]
                for sig in sigs:
                    if len(points) == 0:
                        print("signatures no good or not in right order")
                        return False
                    while points:
                        point = points.pop(0)
                        if point.verify(z, sig):
                            break
                stack.append(encode_num(1))
            except (ValueError, SyntaxError):
                return False
            return True

        def h160_to_p2pkh_address(h160, testnet=False):
            if testnet:
                prefix = b'\x6f'
            else:
                prefix = b'\x00'
            return encode_base58_checksum(prefix + h160)

        def h160_to_p2sh_address(h160, testnet=False):
            if testnet:
                prefix = b'\xc4'
            else:
                prefix = b'\x05'
            return encode_base58_checksum(prefix + h160)

        def sig_hash(self, input_index, redeem_script=None):
            alt_tx_ins = []
            for tx_in in self.tx_ins:
                alt_tx_ins.append(TxIn(
                    prev_tx=tx_in.prev_tx,
                    prev_index=tx_in.prev_index,
                    script_sig=Script([]),
                    sequence=tx_in.sequence,
                ))
            signing_input = alt_tx_ins[input_index]
            if redeem_script:
                print(redeem_script)
                signing_input.script_sig = redeem_script
            else:
                signing_input.script_sig = signing_input.script_pubkey(self.testnet)
            for i in alt_tx_ins:
                print(i.script_sig)
            alt_tx = self.__class__(
                version=self.version,
                tx_ins=alt_tx_ins,
                tx_outs=self.tx_outs,
                locktime=self.locktime)
            result = alt_tx.serialize() + int_to_little_endian(SIGHASH_ALL, 4)
            h256 = hash256(result)
            return int.from_bytes(h256, 'big')

        def verify_input(self, input_index):
            tx_in = self.tx_ins[input_index]
            script_pubkey = tx_in.script_pubkey(testnet=self.testnet)
            if script_pubkey.is_p2sh_script_pubkey():
                element = tx_in.script_sig.instructions[-1]
                raw_redeem = encode_varint(len(element)) + element
                redeem_script = Script.parse(BytesIO(raw_redeem))
            else:
                redeem_script = None
            z = self.sig_hash(input_index, redeem_script)
            script = tx_in.script_sig + script_pubkey
            return script.evaluate(z)

        op.op_checkmultisig = op_checkmultisig
        op.OP_CODE_FUNCTIONS[174] = op_checkmultisig
        helper.h160_to_p2pkh_address = h160_to_p2pkh_address
        helper.h160_to_p2sh_address = h160_to_p2sh_address
        Tx.sig_hash = sig_hash
        Tx.verify_input = verify_input

    def test_example_1(self):
        h160 = bytes.fromhex('74d691da1574e6b3c192ecfb52cc8984ee7b6c56')
        self.assertEqual(
            encode_base58_checksum(b'\x05' + h160),
            '3CLoMMyuoDQTPRD3XYZtCvgvkadrAdvdXh')

    def test_example_2(self):
        blob = bytes.fromhex('0100000001868278ed6ddfb6c1ed3ad5f8181eb0c7a385aa0836f01d5e4789e6bd304d87221a000000475221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152aeffffffff04d3b11400000000001976a914904a49878c0adfc3aa05de7afad2cc15f483a56a88ac7f400900000000001976a914418327e3f3dda4cf5b9089325a4b95abdfa0334088ac722c0c00000000001976a914ba35042cfe9fc66fd35ac2224eebdafd1028ad2788acdc4ace020000000017a91474d691da1574e6b3c192ecfb52cc8984ee7b6c56870000000001000000')
        h256 = hash256(blob)
        z = int.from_bytes(h256, 'big')
        self.assertEqual(z, 0xe71bfa115715d6fd33796948126f40a8cdd39f187e4afb03896795189fe1423c)

    def test_example_3(self):
        blob = bytes.fromhex('0100000001868278ed6ddfb6c1ed3ad5f8181eb0c7a385aa0836f01d5e4789e6bd304d87221a000000475221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152aeffffffff04d3b11400000000001976a914904a49878c0adfc3aa05de7afad2cc15f483a56a88ac7f400900000000001976a914418327e3f3dda4cf5b9089325a4b95abdfa0334088ac722c0c00000000001976a914ba35042cfe9fc66fd35ac2224eebdafd1028ad2788acdc4ace020000000017a91474d691da1574e6b3c192ecfb52cc8984ee7b6c56870000000001000000')
        h256 = hash256(blob)
        z = int.from_bytes(h256, 'big') 
        sec = bytes.fromhex('022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb70')
        der = bytes.fromhex('3045022100dc92655fe37036f47756db8102e0d7d5e28b3beb83a8fef4f5dc0559bddfb94e02205a36d4e4e6c7fcd16658c50783e00c341609977aed3ad00937bf4ee942a89937')
        point = S256Point.parse(sec)
        sig = Signature.parse(der)

    def test_exercise_3(self):
        hex_tx = '0100000001868278ed6ddfb6c1ed3ad5f8181eb0c7a385aa0836f01d5e4789e6bd304d87221a000000db00483045022100dc92655fe37036f47756db8102e0d7d5e28b3beb83a8fef4f5dc0559bddfb94e02205a36d4e4e6c7fcd16658c50783e00c341609977aed3ad00937bf4ee942a8993701483045022100da6bee3c93766232079a01639d07fa869598749729ae323eab8eef53577d611b02207bef15429dcadce2121ea07f233115c6f09034c0be68db99980b9a6c5e75402201475221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152aeffffffff04d3b11400000000001976a914904a49878c0adfc3aa05de7afad2cc15f483a56a88ac7f400900000000001976a914418327e3f3dda4cf5b9089325a4b95abdfa0334088ac722c0c00000000001976a914ba35042cfe9fc66fd35ac2224eebdafd1028ad2788acdc4ace020000000017a91474d691da1574e6b3c192ecfb52cc8984ee7b6c568700000000'
        hex_sec = '03b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb71'
        hex_der = '3045022100da6bee3c93766232079a01639d07fa869598749729ae323eab8eef53577d611b02207bef15429dcadce2121ea07f233115c6f09034c0be68db99980b9a6c5e754022'
        hex_redeem_script = '475221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152ae'
        sec = bytes.fromhex(hex_sec)
        der = bytes.fromhex(hex_der)
        redeem_script = Script.parse(BytesIO(bytes.fromhex(hex_redeem_script)))
        stream = BytesIO(bytes.fromhex(hex_tx))
        tx_obj = Tx.parse(stream)
        tx_obj.tx_ins[0].script_sig = redeem_script
        s = tx_obj.serialize() + int_to_little_endian(SIGHASH_ALL, 4)
        z = int.from_bytes(hash256(s), 'big')
        point = S256Point.parse(sec)
        sig = Signature.parse(der)
        self.assertTrue(point.verify(z, sig))
