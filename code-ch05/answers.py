from io import BytesIO
from unittest import TestCase

from helper import little_endian_to_int, read_varint
from script import Script
from tx import Tx, TxIn, TxOut


methods = []

"""
# tag::exercise1[]
==== Exercise 1

Write the version parsing part of the `parse` method that we've defined. To do this properly, you'll have to convert 4 bytes into a Little-Endian integer.
# end::exercise1[]
# tag::answer1[]
    @classmethod
    def parse(cls, s, testnet=False):
        '''Takes a byte stream and parses the transaction at the start
        return a Tx object
        '''
        version = little_endian_to_int(s.read(4))
        return cls(version, None, None, None, testnet=testnet)
# end::answer1[]
# tag::exercise2[]
==== Exercise 2

Write the inputs parsing part of the `parse` method in `Tx` and the `parse` method for `TxIn`.
# end::exercise2[]
# tag::answer2.1[]
    @classmethod
    def parse(cls, s, testnet=False):
        '''Takes a byte stream and parses the transaction at the start
        return a Tx object
        '''
        version = little_endian_to_int(s.read(4))
        num_inputs = read_varint(s)
        inputs = []
        for _ in range(num_inputs):
            inputs.append(TxIn.parse(s))
        return cls(version, inputs, None, None, testnet=testnet)
# end::answer2.1[]
"""
# tag::answer2.2[]
@classmethod
def parse(cls, s):
    '''Takes a byte stream and parses the tx_input at the start
    return a TxIn object
    '''
    prev_tx = s.read(32)[::-1]
    prev_index = little_endian_to_int(s.read(4))
    script_sig = Script.parse(s)
    sequence = little_endian_to_int(s.read(4))
    return cls(prev_tx, prev_index, script_sig, sequence)
# end::answer2.2[]
methods.append(parse)

"""
# tag::exercise3[]
==== Exercise 3

Write the outputs parsing part of the `parse` method in `Tx` and the `parse` method for `TxOut`.
# end::exercise3[]
# tag::answer3.1[]
class Tx:
...
    @classmethod
    def parse(cls, s, testnet=False):
        '''Takes a byte stream and parses the transaction at the start
        return a Tx object
        '''
        version = little_endian_to_int(s.read(4))
        num_inputs = read_varint(s)
        inputs = []
        for _ in range(num_inputs):
            inputs.append(TxIn.parse(s))
        num_outputs = read_varint(s)
        outputs = []
        for _ in range(num_outputs):
            outputs.append(TxOut.parse(s))
        return cls(version, inputs, outputs, None, testnet=testnet)
# end::answer3.1[]
"""
# tag::answer3.2[]
@classmethod
def parse(cls, s):
    '''Takes a byte stream and parses the tx_output at the start
    return a TxOut object
    '''
    amount = little_endian_to_int(s.read(8))
    script_pubkey = Script.parse(s)
    return cls(amount, script_pubkey)
# end::answer3.2[]
methods.append(parse)

"""
# tag::exercise4[]
==== Exercise 4

Write the locktime parsing part of the `parse` method in `Tx`.
# end::exercise4[]
"""

# tag::answer4[]
@classmethod
def parse(cls, s, testnet=False):
    version = little_endian_to_int(s.read(4))
    num_inputs = read_varint(s)
    inputs = []
    for _ in range(num_inputs):
        inputs.append(TxIn.parse(s))
    num_outputs = read_varint(s)
    outputs = []
    for _ in range(num_outputs):
        outputs.append(TxOut.parse(s))
    locktime = little_endian_to_int(s.read(4))
    return cls(version, inputs, outputs, locktime, testnet=testnet)
# end::answer4[]
methods.append(parse)

"""
# tag::exercise5[]
==== Exercise 5

What is the ScriptSig from the second input, ScriptPubKey from the first output and the amount of the second output for this transaction?

```
010000000456919960ac691763688d3d3bcea9ad6ecaf875df5339e148a1fc61c6e
d7a069e010000006a47304402204585bcdef85e6b1c6af5c2669d4830ff86e42dd2
05c0e089bc2a821657e951c002201024a10366077f87d6bce1f7100ad8cfa8a064b
39d4e8fe4ea13a7b71aa8180f012102f0da57e85eec2934a82a585ea337ce2f4998
b50ae699dd79f5880e253dafafb7feffffffeb8f51f4038dc17e6313cf831d4f022
81c2a468bde0fafd37f1bf882729e7fd3000000006a47304402207899531a52d59a
6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b846
1cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac
96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937feffffff567bf
40595119d1bb8a3037c356efd56170b64cbcc160fb028fa10704b45d77500000000
6a47304402204c7c7818424c7f7911da6cddc59655a70af1cb5eaf17c69dadbfc74
ffa0b662f02207599e08bc8023693ad4e9527dc42c34210f7a7d1d1ddfc8492b654
a11e7620a0012102158b46fbdff65d0172b7989aec8850aa0dae49abfb84c81ae6e
5b251a58ace5cfeffffffd63a5e6c16e620f86f375925b21cabaf736c779f88fd04
dcad51d26690f7f345010000006a47304402200633ea0d3314bea0d95b3cd8dadb2
ef79ea8331ffe1e61f762c0f6daea0fabde022029f23b3e9c30f080446150b23852
028751635dcee2be669c2a1686a4b5edf304012103ffd6f4a67e94aba353a00882e
563ff2722eb4cff0ad6006e86ee20dfe7520d55feffffff0251430f000000000019
76a914ab0c0b2e98b1ab6dbf67d4750b0a56244948a87988ac005a6202000000001
976a9143c82d7df364eb6c75be8c80df2b3eda8db57397088ac46430600
```
# end::exercise5[]
# tag::answer5[]
>>> from io import BytesIO
>>> from tx import Tx
>>> hex_transaction = '0100...00'
>>> stream = BytesIO(bytes.fromhex(hex_transaction))
>>> tx_obj = Tx.parse(stream)
>>> print(tx_obj.tx_ins[1].script_sig)
304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc
26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071
c1a71601 035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43
c15a2937
>>> print(tx_obj.tx_outs[0].script_pubkey)
OP_DUP OP_HASH160 ab0c0b2e98b1ab6dbf67d4750b0a56244948a879 OP_EQUAL
VERIFY OP_CHECKSIG
>>> print(tx_obj.tx_outs[1].amount)
40000000

# end::answer5[]
# tag::exercise6[]
==== Exercise 6

Write the `fee` method for the `Tx` class.
# end::exercise6[]
"""

# tag::answer6[]
def fee(self, testnet=False):
    input_sum, output_sum = 0, 0
    for tx_in in self.tx_ins:
        input_sum += tx_in.value(testnet=testnet)
    for tx_out in self.tx_outs:
        output_sum += tx_out.amount
    return input_sum - output_sum
# end::answer6[]

class Chapter5Test(TestCase):

    def test_apply(self):
        TxIn.parse = methods[0]
        TxOut.parse = methods[1]
        Tx.parse = methods[2]
        Tx.fee = fee
