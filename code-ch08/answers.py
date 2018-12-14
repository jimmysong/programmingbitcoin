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


'''
# tag::exercise1[]
==== Exercise 1

Write the `op_checkmultisig` function of `op.py`.
# end::exercise1[]
'''

# tag::answer1[]
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
                return False
            while points:
                point = points.pop(0)
                if point.verify(z, sig):
                    break
        stack.append(encode_num(1))
    except (ValueError, SyntaxError):
        return False
    return True
# end::answer1[]

'''
# tag::exercise2[]
==== Exercise 2

Write `h160_to_p2pkh_address` that converts a 20-byte hash160 into a p2pkh address.
# end::exercise2[]
'''

# tag::answer2[]
def h160_to_p2pkh_address(h160, testnet=False):
    if testnet:
        prefix = b'\x6f'
    else:
        prefix = b'\x00'
    return encode_base58_checksum(prefix + h160)
# end::answer2[]

'''
# tag::exercise3[]
==== Exercise 3

Write `h160_to_p2sh_address` that converts a 20-byte hash160 into a p2sh address.
# end::exercise3[]
'''

# tag::answer3[]
def h160_to_p2sh_address(h160, testnet=False):
    if testnet:
        prefix = b'\xc4'
    else:
        prefix = b'\x05'
    return encode_base58_checksum(prefix + h160)
# end::answer3[]

'''
# tag::exercise5[]
==== Exercise 5

Modify the `sig_hash` and `verify_input` methods to be able to verify p2sh transactions.
# end::exercise5[]
'''

# tag::answer5[]
def sig_hash(self, input_index, redeem_script=None):
    '''Returns the integer representation of the hash that needs to get
    signed for index input_index'''
    s = int_to_little_endian(self.version, 4)
    s += encode_varint(len(self.tx_ins))
    for i, tx_in in enumerate(self.tx_ins):
        if i == input_index:
            if redeem_script:
                script_sig = redeem_script
            else:
                script_sig = tx_in.script_pubkey(self.testnet)
        else:
            script_sig = None
        s += TxIn(
            prev_tx=tx_in.prev_tx,
            prev_index=tx_in.prev_index,
            script_sig=script_sig,
            sequence=tx_in.sequence,
        ).serialize()
    s += encode_varint(len(self.tx_outs))
    for tx_out in self.tx_outs:
        s += tx_out.serialize()
    s += int_to_little_endian(self.locktime, 4)
    s += int_to_little_endian(SIGHASH_ALL, 4)
    h256 = hash256(s)
    return int.from_bytes(h256, 'big')

def verify_input(self, input_index):
    tx_in = self.tx_ins[input_index]
    script_pubkey = tx_in.script_pubkey(testnet=self.testnet)
    if script_pubkey.is_p2sh_script_pubkey():
        instruction = tx_in.script_sig.instructions[-1]
        raw_redeem = encode_varint(len(instruction)) + instruction
        redeem_script = Script.parse(BytesIO(raw_redeem))
    else:
        redeem_script = None
    z = self.sig_hash(input_index, redeem_script)
    combined = tx_in.script_sig + script_pubkey
    return combined.evaluate(z)
# end::answer5[]


class DocTest:
    '''
    # tag::exercise4[]
    ==== Exercise 4

    Validate the second signature from the transaction above.
    # end::exercise4[]
    # tag::answer4[]
    >>> from io import BytesIO
    >>> from ecc import S256Point, Signature
    >>> from helper import hash256, int_to_little_endian
    >>> from script import Script
    >>> from tx import Tx, SIGHASH_ALL
    >>> hex_tx = '0100000001868278ed6ddfb6c1ed3ad5f8181eb0c7a385aa0836f01d5e47\
89e6bd304d87221a000000db00483045022100dc92655fe37036f47756db8102e0d7d5e28b3beb\
83a8fef4f5dc0559bddfb94e02205a36d4e4e6c7fcd16658c50783e00c341609977aed3ad00937\
bf4ee942a8993701483045022100da6bee3c93766232079a01639d07fa869598749729ae323eab\
8eef53577d611b02207bef15429dcadce2121ea07f233115c6f09034c0be68db99980b9a6c5e75\
402201475221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb70\
2103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152aeffffff\
ff04d3b11400000000001976a914904a49878c0adfc3aa05de7afad2cc15f483a56a88ac7f4009\
00000000001976a914418327e3f3dda4cf5b9089325a4b95abdfa0334088ac722c0c0000000000\
1976a914ba35042cfe9fc66fd35ac2224eebdafd1028ad2788acdc4ace020000000017a91474d6\
91da1574e6b3c192ecfb52cc8984ee7b6c568700000000'
    >>> hex_sec = '03b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbd\
bd4bb71'
    >>> hex_der = '3045022100da6bee3c93766232079a01639d07fa869598749729ae323ea\
b8eef53577d611b02207bef15429dcadce2121ea07f233115c6f09034c0be68db99980b9a6c5e7\
54022'
    >>> hex_redeem_script = '475221022626e955ea6ea6d98850c994f9107b036b1334f18\
ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ff\
ac7fbdbd4bb7152ae'
    >>> sec = bytes.fromhex(hex_sec)
    >>> der = bytes.fromhex(hex_der)
    >>> redeem_script = Script.parse(BytesIO(bytes.fromhex(hex_redeem_script)))
    >>> stream = BytesIO(bytes.fromhex(hex_tx))
    >>> tx_obj = Tx.parse(stream)
    >>> s = int_to_little_endian(tx_obj.version, 4)
    >>> s += encode_varint(len(tx_obj.tx_ins))
    >>> i = tx_obj.tx_ins[0]
    >>> s += TxIn(i.prev_tx, i.prev_index, redeem_script, i.sequence).serialize()
    >>> s += encode_varint(len(tx_obj.tx_outs))
    >>> for tx_out in tx_obj.tx_outs:
    ...    s += tx_out.serialize()
    >>> s += int_to_little_endian(tx_obj.locktime, 4)
    >>> s += int_to_little_endian(SIGHASH_ALL, 4)
    >>> z = int.from_bytes(hash256(s), 'big')
    >>> point = S256Point.parse(sec)
    >>> sig = Signature.parse(der)
    >>> print(point.verify(z, sig))
    True

    # end::answer4[]
    '''


class ChapterTest(TestCase):

    def test_apply(self):
        op.op_checkmultisig = op_checkmultisig
        op.OP_CODE_FUNCTIONS[174] = op_checkmultisig
        helper.h160_to_p2pkh_address = h160_to_p2pkh_address
        helper.h160_to_p2sh_address = h160_to_p2sh_address
        Tx.sig_hash = sig_hash
        Tx.verify_input = verify_input
