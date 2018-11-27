from unittest import TestCase

from ecc import PrivateKey, Signature
from helper import encode_base58, hash256

import helper


def ltoi(b):
    return int.from_bytes(b, 'little')

def itol(n, length):
    return n.to_bytes(length, 'little')


class Chapter4Test(TestCase):

    def test_apply(self):
        helper.little_endian_to_int = ltoi
        helper.int_to_little_endian = itol

    def test_exercise_1(self):
        priv = PrivateKey(5000)
        self.assertEqual(priv.point.sec(compressed=False).hex(), '04ffe558e388852f0120e46af2d1b370f85854a8eb0841811ece0e3e03d282d57c315dc72890a4f10a1481c031b03b351b0dc79901ca18a00cf009dbdb157a1d10')
        priv = PrivateKey(2018**5)
        self.assertEqual(priv.point.sec(compressed=False).hex(), '04027f3da1918455e03c46f659266a1bb5204e959db7364d2f473bdf8f0a13cc9dff87647fd023c13b4a4994f17691895806e1b40b57f4fd22581a4f46851f3b06')
        priv = PrivateKey(0xdeadbeef12345)
        self.assertEqual(priv.point.sec(compressed=False).hex(), '04d90cd625ee87dd38656dd95cf79f65f60f7273b67d3096e68bd81e4f5342691f842efa762fd59961d0e99803c61edba8b3e3f7dc3a341836f97733aebf987121')

    def test_exercise_2(self):
        priv = PrivateKey(5001)
        self.assertEqual(priv.point.sec(compressed=True).hex(), '0357a4f368868a8a6d572991e484e664810ff14c05c0fa023275251151fe0e53d1')
        priv = PrivateKey(2019**5)
        self.assertEqual(priv.point.sec(compressed=True).hex(), '02933ec2d2b111b92737ec12f1c5d20f3233a0ad21cd8b36d0bca7a0cfa5cb8701')
        priv = PrivateKey(0xdeadbeef54321)
        self.assertEqual(priv.point.sec(compressed=True).hex(), '0296be5b1292f6c856b3c5654e886fc13511462059089cdf9c479623bfcbe77690')

    def test_exercise_3(self):
        r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
        s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        sig = Signature(r, s)
        self.assertEqual(sig.der().hex(), '3045022037206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec')

    def test_exercise_4(self):
        h = '7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d'
        self.assertEqual(encode_base58(bytes.fromhex(h)).decode('ascii'), '9MA8fRQrT4u8Zj8ZRd6MAiiyaxb2Y1CMpvVkHQu5hVM6')
        h = 'eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c'
        self.assertEqual(encode_base58(bytes.fromhex(h)).decode('ascii'), '4fE3H2E6XMp4SsxtwinF7w9a34ooUrwWe4WsW1458Pd')
        h = 'c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6'
        self.assertEqual(encode_base58(bytes.fromhex(h)).decode('ascii'), 'EQJsjkd6JaGwxrjEhfeqPenqHwrBmPQZjJGNSCHBkcF7')

    def test_exercise_5(self):
        priv = PrivateKey(5002)
        self.assertEqual(priv.point.address(compressed=False, testnet=True), 'mmTPbXQFxboEtNRkwfh6K51jvdtHLxGeMA')
        priv = PrivateKey(2020**5)
        self.assertEqual(priv.point.address(compressed=True, testnet=True), 'mopVkxp8UhXqRYbCYJsbeE1h1fiF64jcoH')
        priv = PrivateKey(0x12345deadbeef)
        self.assertEqual(priv.point.address(compressed=True, testnet=False), '1F1Pn2y6pDb68E5nYJJeba4TLg2U7B6KF1')

    def test_exercise_6(self):
        priv = PrivateKey(5003)
        self.assertEqual(priv.wif(compressed=True, testnet=True), 'cMahea7zqjxrtgAbB7LSGbcQUr1uX1ojuat9jZodMN8rFTv2sfUK')
        priv = PrivateKey(2021**5)
        self.assertEqual(priv.wif(compressed=False, testnet=True), '91avARGdfge8E4tZfYLoxeJ5sGBdNJQH4kvjpWAxgzczjbCwxic')
        priv = PrivateKey(0x54321deadbeef)
        self.assertEqual(priv.wif(compressed=True, testnet=False), 'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgiuQJv1h8Ytr2S53a')

    def test_exercise_9(self):
        passphrase = b'jimmy@programmingblockchain.com my secret'
        secret = helper.little_endian_to_int(hash256(passphrase))
        priv = PrivateKey(secret)
        self.assertEqual(priv.point.address(testnet=True), 'mft9LRNtaBNtpkknB8xgm17UvPedZ4ecYL')
