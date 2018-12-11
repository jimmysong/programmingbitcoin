from io import BytesIO
from unittest import TestCase

from ecc import PrivateKey, S256Point, Signature
from helper import (
    decode_base58,
    encode_varint,
    hash256,
    int_to_little_endian,
    SIGHASH_ALL,
)
from script import p2pkh_script, Script
from tx import Tx, TxIn, TxOut

"""
# tag::exercise1[]
==== Exercise 1

Write the `sig_hash` method for the `Tx` class.
# end::exercise1[]
"""

# tag::answer1[]
def sig_hash(self, input_index):
    s = int_to_little_endian(self.version, 4)
    s += encode_varint(len(self.tx_ins))
    for i, tx_in in enumerate(self.tx_ins):
        if i == input_index:
            s += TxIn(
                prev_tx=tx_in.prev_tx,
                prev_index=tx_in.prev_index,
                script_sig=tx_in.script_pubkey(self.testnet),
                sequence=tx_in.sequence,
            ).serialize()
        else:
            s += TxIn(
                prev_tx=tx_in.prev_tx,
                prev_index=tx_in.prev_index,
                sequence=tx_in.sequence,
            ).serialize()
    s += encode_varint(len(self.tx_outs))
    for tx_out in self.tx_outs:
        s += tx_out.serialize()
    s += int_to_little_endian(self.locktime, 4)
    s += int_to_little_endian(SIGHASH_ALL, 4)
    h256 = hash256(s)
    return int.from_bytes(h256, 'big')
# end::answer1[]

"""
# tag::exercise2[]
==== Exercise 2

Write the `verify_input` method for the `Tx` class. You will want to use the `TxIn.script_pubkey()`, `Tx.sig_hash()` and `Script.evaluate()` methods.
# end::exercise2[]
"""

# tag::answer2[]
def verify_input(self, input_index):
    tx_in = self.tx_ins[input_index]
    script_pubkey = tx_in.script_pubkey(testnet=self.testnet)
    z = self.sig_hash(input_index)
    combined = tx_in.script_sig + script_pubkey
    return combined.evaluate(z)
# end::answer2[]

"""
# tag::exercise3[]
==== Exercise 3

Write the `sign_input` method for the `Tx` class.
# end::exercise3[]
"""

# tag::answer3[]
def sign_input(self, input_index, private_key):
    z = self.sig_hash(input_index)
    der = private_key.sign(z).der()
    sig = der + SIGHASH_ALL.to_bytes(1, 'big')
    sec = private_key.point.sec()
    self.tx_ins[input_index].script_sig = Script([sig, sec])
    return self.verify_input(input_index)
# end::answer3[]

"""
# tag::exercise4[]
==== Exercise 4

Create a testnet transaction that sends 60% of a single UTXO to `mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv`. The remaining amount minus fees should go back to your own change address. This should be a 1 input, 2 output transaction.

You can broadcast the transaction at https://testnet.blockchain.info/pushtx
# end::exercise4[]
# tag::answer4[]
>>> from ecc import PrivateKey
>>> from helper import decode_base58, SIGHASH_ALL
>>> from script import p2pkh_script, Script
>>> from tx import TxIn, TxOut, Tx
>>> prev_tx = bytes.fromhex('75a1c4bc671f55f626dda1074c7725991e6f68b8fcefcfca7b64405ca3b45f1c')
>>> prev_index = 1
>>> target_address = 'miKegze5FQNCnGw6PKyqUbYUeBa4x2hFeM'
>>> target_amount = 0.01
>>> change_address = 'mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2'
>>> change_amount = 0.009
>>> secret = 8675309
>>> priv = PrivateKey(secret=secret)
>>> tx_ins = []
>>> tx_ins.append(TxIn(prev_tx, prev_index))
>>> tx_outs = []
>>> h160 = decode_base58(target_address)
>>> script_pubkey = p2pkh_script(h160)
>>> target_satoshis = int(target_amount*100000000)
>>> tx_outs.append(TxOut(target_satoshis, script_pubkey))
>>> h160 = decode_base58(change_address)
>>> script_pubkey = p2pkh_script(h160)
>>> change_satoshis = int(change_amount*100000000)
>>> tx_outs.append(TxOut(change_satoshis, script_pubkey))
>>> tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True)
>>> tx_obj.sign_input(0, priv)
>>> print(tx_obj.serialize().hex())
01000000011c5fb4a35c40647bcacfeffcb8686f1e9925774c07a1dd26f6551f67bcc4a175010000006b483045022100b610b6df76364e1fcad579a862152623cb364d6409fe59e1922da69f32a8520b022059007da287d10088b39f487764f9d04160ece1ae551d5c7b4b2cb5f03cd44f55012103935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67ffffffff0240420f00000000001976a9141ec51b3654c1f1d0f4929d11a1f702937eaf50c888ac9fbb0d00000000001976a914d52ad7ca9b3d096a38e752c2018e6fbc40cdf26f88ac00000000

# end::answer4[]
# tag::exercise5[]
==== Exercise 5

Advanced: get some more testnet coins from a testnet faucet and create a 2 input, 1 output transaction. 1 input should be from the faucet, the other should be from the previous exercise, the output can be your own address.

You can broadcast the transaction at https://testnet.blockchain.info/pushtx
# end::exercise5[]
# tag::answer5[]
>>> from ecc import PrivateKey
>>> from helper import decode_base58, SIGHASH_ALL
>>> from script import p2pkh_script, Script
>>> from tx import TxIn, TxOut, Tx
>>> prev_tx_1 = bytes.fromhex('11d05ce707c1120248370d1cbf5561d22c4f83aeba0436792c82e0bd57fe2a2f')
>>> prev_index_1 = 1
>>> prev_tx_2 = bytes.fromhex('51f61f77bd061b9a0da60d4bedaaf1b1fad0c11e65fdc744797ee22d20b03d15')
>>> prev_index_2 = 1
>>> target_address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'
>>> target_amount = 0.0429
>>> secret = 8675309
>>> priv = PrivateKey(secret=secret)
>>> tx_ins = []
>>> tx_ins.append(TxIn(prev_tx_1, prev_index_1))
>>> tx_ins.append(TxIn(prev_tx_2, prev_index_2))
>>> tx_outs = []
>>> h160 = decode_base58(target_address)
>>> script_pubkey = p2pkh_script(h160)
>>> target_satoshis = int(target_amount*100000000)
>>> tx_outs.append(TxOut(target_satoshis, script_pubkey))
>>> tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True)
>>> tx_obj.sign_input(0, priv)
>>> tx_obj.sign_input(1, priv)
>>> print(tx_obj.serialize().hex())
01000000022f2afe57bde0822c793604baae834f2cd26155bf1c0d37480212c107e75cd011010000006b483045022100dddbb9f2ae014631a80265b133369ff2aa9e429cf2188e66f4256cab60062caa02200889b7494b5343dadcdfdab335c585f0ebd600a0ac8792ea06c8a3c00420eea1012103935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67ffffffff153db0202de27e7944c7fd651ec1d0fab1f1aaed4b0da60d9a1b06bd771ff651010000006b483045022100bb3ad8379b0729fe23b867b7ad49e72ddf5d040bafcf6479463c9b4ea0e7f07b02202ba53fa490602b41b0f37ac0aaf20dfe909d761868e5721739ce392f9c6dd268012103935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67ffffffff01d0754100000000001976a914ad346f8eb57dee9a37981716e498120ae80e44f788ac00000000

# end::answer5[]
"""



class Chapter7Test(TestCase):

    def test_apply(self):
        Tx.sig_hash = sig_hash
        Tx.verify_input = verify_input
        Tx.sign_input = sign_input
