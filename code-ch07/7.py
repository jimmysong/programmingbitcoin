from io import BytesIO
from unittest import TestCase

from ecc import PrivateKey, S256Point, Signature
from helper import (
    decode_base58,
    hash256,
    int_to_little_endian,
    SIGHASH_ALL,
)
from script import p2pkh_script, Script
from tx import Tx, TxIn, TxOut


class Chapter7Test(TestCase):

    def test_apply(self):

        def sig_hash(self, input_index, hash_type):
            alt_tx_ins = []
            for tx_in in self.tx_ins:
                alt_tx_ins.append(TxIn(
                    prev_tx=tx_in.prev_tx,
                    prev_index=tx_in.prev_index,
                    script_sig=Script([]),
                    sequence=tx_in.sequence,
                ))
            signing_input = alt_tx_ins[input_index]
            signing_input.script_sig = signing_input.script_pubkey(self.testnet)
            alt_tx = self.__class__(
                version=self.version,
                tx_ins=alt_tx_ins,
                tx_outs=self.tx_outs,
                locktime=self.locktime,
	    )
            result = alt_tx.serialize() + int_to_little_endian(hash_type, 4)
            h256 = hash256(result)
            return int.from_bytes(h256, 'big')

        def verify_input(self, input_index):
            tx_in = self.tx_ins[input_index]
            script_pubkey = tx_in.script_pubkey(testnet=self.testnet)
            z = self.sig_hash(input_index, SIGHASH_ALL)
            combined = tx_in.script_sig + script_pubkey
            return combined.evaluate(z)

        def sign_input(self, input_index, private_key, hash_type):
            z = self.sig_hash(input_index, hash_type)
            der = private_key.sign(z).der()
            sig = der + hash_type.to_bytes(1, 'big')
            sec = private_key.point.sec()
            self.tx_ins[input_index].script_sig = Script([sig, sec])
            return self.verify_input(input_index)

        Tx.sig_hash = sig_hash
        Tx.verify_input = verify_input
        Tx.sign_input = sign_input

    def test_example_1(self):
        stream = BytesIO(bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600'))
        transaction = Tx.parse(stream)
        self.assertTrue(transaction.fee() >= 0)

    def test_example_2(self):
        sec = bytes.fromhex('0349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
        der = bytes.fromhex('3045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed')
        z = 0x27e0c5994dec7824e56dec6b2fcb342eb7cdb0d0957c2fce9882f715e85d81a6
        point = S256Point.parse(sec)
        signature = Signature.parse(der)
        self.assertTrue(point.verify(z, signature))

    def test_example_3(self):
        blob = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000001976a914a802fc56c704ce87c42d7c92eb75e7896bdc41ae88acfeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac1943060001000000')
        h256 = hash256(blob)
        z = int.from_bytes(h256, 'big')
        self.assertEqual(z, 0x27e0c5994dec7824e56dec6b2fcb342eb7cdb0d0957c2fce9882f715e85d81a6)

    def test_example_4(self):
        sec = bytes.fromhex('0349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
        der = bytes.fromhex('3045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed')
        z = 0x27e0c5994dec7824e56dec6b2fcb342eb7cdb0d0957c2fce9882f715e85d81a6
        point = S256Point.parse(sec)
        signature = Signature.parse(der)
        self.assertTrue(point.verify(z, signature))

    def test_example_5(self):
        tx_ins = []
        prev_tx = bytes.fromhex('0d6fe5213c0b3291f208cba8bfb59b7476dffacc4e5cb66f6eb20a080843a299')
        prev_index = 13
        tx_ins.append(TxIn(prev_tx, prev_index, Script([]), 0xffffffff))
        tx_outs = []
        change_amount = int(0.33*100000000)
        change_h160 = decode_base58('mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2')
        change_script = p2pkh_script(change_h160)
        tx_outs.append(TxOut(amount=change_amount, script_pubkey=change_script))
        target_amount = int(0.1*100000000)
        target_h160 = decode_base58('mnrVtF8DWjMu839VW3rBfgYaAfKk8983Xf')
        target_script = p2pkh_script(target_h160)
        tx_outs.append(TxOut(amount=target_amount, script_pubkey=target_script))
        transaction = Tx(1, tx_ins, tx_outs, 0, testnet=True)
        want = '010000000199a24308080ab26e6fb65c4eccfadf76749bb5bfa8cb08f291320b3c21e56f0d0d00000000ffffffff02408af701000000001976a914d52ad7ca9b3d096a38e752c2018e6fbc40cdf26f88ac80969800000000001976a914507b27411ccf7f16f10297de6cef3f291623eddf88ac00000000'
        self.assertEqual(transaction.serialize().hex(), want)

    def test_example_6(self):
        tx_ins = []
        prev_tx = bytes.fromhex('0d6fe5213c0b3291f208cba8bfb59b7476dffacc4e5cb66f6eb20a080843a299')
        prev_index = 13
        tx_ins.append(TxIn(prev_tx, prev_index, Script([]), 0xffffffff))
        tx_outs = []
        change_amount = int(0.33*100000000)
        change_h160 = decode_base58('mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2')
        change_script = p2pkh_script(change_h160)
        tx_outs.append(TxOut(amount=change_amount, script_pubkey=change_script))
        target_amount = int(0.1*100000000)
        target_h160 = decode_base58('mnrVtF8DWjMu839VW3rBfgYaAfKk8983Xf')
        target_script = p2pkh_script(target_h160)
        tx_outs.append(TxOut(amount=target_amount, script_pubkey=target_script))
        transaction = Tx(1, tx_ins, tx_outs, 0, testnet=True)
        z = transaction.sig_hash(0, SIGHASH_ALL)
        private_key = PrivateKey(secret=8675309)
        der = private_key.sign(z).der()
        sig = der + SIGHASH_ALL.to_bytes(1, 'big')
        sec = private_key.point.sec()
        transaction.tx_ins[0].script_sig = Script([sig, sec])
        want = '010000000199a24308080ab26e6fb65c4eccfadf76749bb5bfa8cb08f291320b3c21e56f0d0d0000006b4830450221008ed46aa2cf12d6d81065bfabe903670165b538f65ee9a3385e6327d80c66d3b502203124f804410527497329ec4715e18558082d489b218677bd029e7fa306a72236012103935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67ffffffff02408af701000000001976a914d52ad7ca9b3d096a38e752c2018e6fbc40cdf26f88ac80969800000000001976a914507b27411ccf7f16f10297de6cef3f291623eddf88ac00000000'
        self.assertEqual(transaction.serialize().hex(), want)

    def test_example_7(self):
        private_key = PrivateKey(secret=90210)
        self.assertEqual(
            private_key.point.address(testnet=True),
            'mqNK1JUujDXeufN9bDVKtzzvriqjnZLxHU')

    def test_exercise_4(self):
        prev_tx = bytes.fromhex('75a1c4bc671f55f626dda1074c7725991e6f68b8fcefcfca7b64405ca3b45f1c')
        prev_index = 1
        target_address = 'miKegze5FQNCnGw6PKyqUbYUeBa4x2hFeM'
        target_amount = 0.01
        change_address = 'mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2'
        change_amount = 0.009
        secret = 8675309
        priv = PrivateKey(secret=secret)
        tx_ins = []
        tx_ins.append(TxIn(prev_tx, prev_index, Script([]), 0xffffffff))
        tx_outs = []
        h160 = decode_base58(target_address)
        script_pubkey = p2pkh_script(h160)
        target_satoshis = int(target_amount*100000000)
        tx_outs.append(TxOut(target_satoshis, script_pubkey))
        h160 = decode_base58(change_address)
        script_pubkey = p2pkh_script(h160)
        change_satoshis = int(change_amount*100000000)
        tx_outs.append(TxOut(change_satoshis, script_pubkey))
        tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True)
        self.assertTrue(tx_obj.sign_input(0, priv, SIGHASH_ALL))
        self.assertTrue(tx_obj.verify())
        want = '01000000011c5fb4a35c40647bcacfeffcb8686f1e9925774c07a1dd26f6551f67bcc4a175010000006b483045022100a08ebb92422b3599a2d2fcdaa11f8f807a66ccf33e7f4a9ff0a3c51f1b1ec5dd02205ed21dfede5925362b8d9833e908646c54be7ac6664e31650159e8f69b6ca539012103935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67ffffffff0240420f00000000001976a9141ec51b3654c1f1d0f4929d11a1f702937eaf50c888ac9fbb0d00000000001976a914d52ad7ca9b3d096a38e752c2018e6fbc40cdf26f88ac00000000'
        self.assertEqual(tx_obj.serialize().hex(), want)

    def test_exercise_5(self):
        prev_tx_1 = bytes.fromhex('11d05ce707c1120248370d1cbf5561d22c4f83aeba0436792c82e0bd57fe2a2f')
        prev_index_1 = 1
        prev_tx_2 = bytes.fromhex('51f61f77bd061b9a0da60d4bedaaf1b1fad0c11e65fdc744797ee22d20b03d15')
        prev_index_2 = 1
        target_address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'
        target_amount = 0.0429
        secret = 8675309
        priv = PrivateKey(secret=secret)
        tx_ins = []
        tx_ins.append(TxIn(prev_tx_1, prev_index_1, Script([]), 0xffffffff))
        tx_ins.append(TxIn(prev_tx_2, prev_index_2, Script([]), 0xffffffff))
        tx_outs = []
        h160 = decode_base58(target_address)
        script_pubkey = p2pkh_script(h160)
        target_satoshis = int(target_amount*100000000)
        tx_outs.append(TxOut(target_satoshis, script_pubkey))
        tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True)
        self.assertTrue(tx_obj.sign_input(0, priv, SIGHASH_ALL))
        self.assertTrue(tx_obj.sign_input(1, priv, SIGHASH_ALL))
        self.assertTrue(tx_obj.verify())
        want = '01000000022f2afe57bde0822c793604baae834f2cd26155bf1c0d37480212c107e75cd011010000006a47304402204cc5fe11b2b025f8fc9f6073b5e3942883bbba266b71751068badeb8f11f0364022070178363f5dea4149581a4b9b9dbad91ec1fd990e3fa14f9de3ccb421fa5b269012103935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67ffffffff153db0202de27e7944c7fd651ec1d0fab1f1aaed4b0da60d9a1b06bd771ff651010000006b483045022100b7a938d4679aa7271f0d32d83b61a85eb0180cf1261d44feaad23dfd9799dafb02205ff2f366ddd9555f7146861a8298b7636be8b292090a224c5dc84268480d8be1012103935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67ffffffff01d0754100000000001976a914ad346f8eb57dee9a37981716e498120ae80e44f788ac00000000'
        self.assertEqual(tx_obj.serialize().hex(), want)

