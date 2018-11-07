from io import BytesIO
from unittest import TestCase

from helper import little_endian_to_int, read_varint
from script import Script
from tx import Tx, TxIn, TxOut


class Chapter5Test(TestCase):

    def test_apply(self):

        @classmethod
        def tx_parse(cls, s, testnet=False):
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

        @classmethod
        def tx_in_parse(cls, s):
            prev_tx = s.read(32)[::-1]
            prev_index = little_endian_to_int(s.read(4))
            script_sig = Script.parse(s)
            sequence = little_endian_to_int(s.read(4))
            return cls(prev_tx, prev_index, script_sig, sequence)
        
        @classmethod
        def tx_out_parse(cls, s):
            amount = little_endian_to_int(s.read(8))
            script_pubkey = Script.parse(s)
            return cls(amount, script_pubkey)

        def fee(self, testnet=False):
            input_sum, output_sum = 0, 0
            for tx_in in self.tx_ins:
                input_sum += tx_in.value(testnet=testnet)
            for tx_out in self.tx_outs:
                output_sum += tx_out.amount
            return input_sum - output_sum

        Tx.parse = tx_parse
        Tx.fee = fee
        TxIn.parse = tx_in_parse
        TxOut.parse = tx_out_parse

    def test_example_1(self):
        script_hex = '6b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a'
        stream = BytesIO(bytes.fromhex(script_hex))
        script_sig = Script.parse(stream)
        self.assertEqual(script_sig.instructions[0].hex(), '3045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01')
        self.assertEqual(script_sig.instructions[1].hex(), '0349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')

    def test_exercise_5(self):
        hex_transaction = '010000000456919960ac691763688d3d3bcea9ad6ecaf875df5339e148a1fc61c6ed7a069e010000006a47304402204585bcdef85e6b1c6af5c2669d4830ff86e42dd205c0e089bc2a821657e951c002201024a10366077f87d6bce1f7100ad8cfa8a064b39d4e8fe4ea13a7b71aa8180f012102f0da57e85eec2934a82a585ea337ce2f4998b50ae699dd79f5880e253dafafb7feffffffeb8f51f4038dc17e6313cf831d4f02281c2a468bde0fafd37f1bf882729e7fd3000000006a47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937feffffff567bf40595119d1bb8a3037c356efd56170b64cbcc160fb028fa10704b45d775000000006a47304402204c7c7818424c7f7911da6cddc59655a70af1cb5eaf17c69dadbfc74ffa0b662f02207599e08bc8023693ad4e9527dc42c34210f7a7d1d1ddfc8492b654a11e7620a0012102158b46fbdff65d0172b7989aec8850aa0dae49abfb84c81ae6e5b251a58ace5cfeffffffd63a5e6c16e620f86f375925b21cabaf736c779f88fd04dcad51d26690f7f345010000006a47304402200633ea0d3314bea0d95b3cd8dadb2ef79ea8331ffe1e61f762c0f6daea0fabde022029f23b3e9c30f080446150b23852028751635dcee2be669c2a1686a4b5edf304012103ffd6f4a67e94aba353a00882e563ff2722eb4cff0ad6006e86ee20dfe7520d55feffffff0251430f00000000001976a914ab0c0b2e98b1ab6dbf67d4750b0a56244948a87988ac005a6202000000001976a9143c82d7df364eb6c75be8c80df2b3eda8db57397088ac46430600'
        stream = BytesIO(bytes.fromhex(hex_transaction))
        tx_obj = Tx.parse(stream)
        self.assertEqual(
            tx_obj.tx_ins[1].script_sig.instructions[0].hex(),
'304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a71601')
        self.assertEqual(
            tx_obj.tx_ins[1].script_sig.instructions[1].hex(),
            '035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937')
        self.assertEqual(tx_obj.tx_outs[0].script_pubkey.instructions[0], 0x76)
        self.assertEqual(tx_obj.tx_outs[0].script_pubkey.instructions[1], 0xa9)
        self.assertEqual(
            tx_obj.tx_outs[0].script_pubkey.instructions[2].hex(),
            'ab0c0b2e98b1ab6dbf67d4750b0a56244948a879')
        self.assertEqual(tx_obj.tx_outs[0].script_pubkey.instructions[3], 0x88)
        self.assertEqual(tx_obj.tx_outs[0].script_pubkey.instructions[4], 0xac)
        self.assertEqual(tx_obj.tx_outs[1].amount, 40000000)
