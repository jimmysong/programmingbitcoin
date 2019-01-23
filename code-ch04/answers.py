'''
# tag::exercise1[]
==== Exercise 1

Find the uncompressed SEC format for the public key where the private key secrets are:

* 5,000
* 2,018^5^
* 0xdeadbeef12345
# end::exercise1[]
# tag::answer1[]
>>> from ecc import PrivateKey
>>> priv = PrivateKey(5000)
>>> print(priv.point.sec(compressed=False).hex())
04ffe558e388852f0120e46af2d1b370f85854a8eb0841811ece0e3e03d282d57c315dc72890a4\
f10a1481c031b03b351b0dc79901ca18a00cf009dbdb157a1d10
>>> priv = PrivateKey(2018**5)
>>> print(priv.point.sec(compressed=False).hex())
04027f3da1918455e03c46f659266a1bb5204e959db7364d2f473bdf8f0a13cc9dff87647fd023\
c13b4a4994f17691895806e1b40b57f4fd22581a4f46851f3b06
>>> priv = PrivateKey(0xdeadbeef12345)
>>> print(priv.point.sec(compressed=False).hex())
04d90cd625ee87dd38656dd95cf79f65f60f7273b67d3096e68bd81e4f5342691f842efa762fd5\
9961d0e99803c61edba8b3e3f7dc3a341836f97733aebf987121

# end::answer1[]
# tag::exercise2[]
==== Exercise 2

Find the Compressed SEC format for the public key where the private key secrets are:

* 5,001
* 2,019^5^
* 0xdeadbeef54321
# end::exercise2[]
# tag::answer2[]
>>> from ecc import PrivateKey
>>> priv = PrivateKey(5001)
>>> print(priv.point.sec(compressed=True).hex())
0357a4f368868a8a6d572991e484e664810ff14c05c0fa023275251151fe0e53d1
>>> priv = PrivateKey(2019**5)
>>> print(priv.point.sec(compressed=True).hex())
02933ec2d2b111b92737ec12f1c5d20f3233a0ad21cd8b36d0bca7a0cfa5cb8701
>>> priv = PrivateKey(0xdeadbeef54321)
>>> print(priv.point.sec(compressed=True).hex())
0296be5b1292f6c856b3c5654e886fc13511462059089cdf9c479623bfcbe77690

# end::answer2[]
# tag::exercise3[]
==== Exercise 3

Find the DER format for a signature whose `r` and `s` values are:

* `r` = pass:[<br/>]`0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6`

* `s` = pass:[<br/>]`0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec`
# end::exercise3[]
# tag::answer3[]
>>> from ecc import Signature
>>> r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
>>> s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
>>> sig = Signature(r,s)
>>> print(sig.der().hex())
3045022037206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6022100\
8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec

# end::answer3[]
# tag::exercise4[]
==== Exercise 4

Convert the following hex to binary and then to Base58:

* `7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d`
* `eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c`
* `c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6`
# end::exercise4[]
# tag::answer4[]
>>> from helper import encode_base58
>>> h = '7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d'
>>> print(encode_base58(bytes.fromhex(h)).decode('ascii'))
9MA8fRQrT4u8Zj8ZRd6MAiiyaxb2Y1CMpvVkHQu5hVM6
>>> h = 'eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c'
>>> print(encode_base58(bytes.fromhex(h)).decode('ascii'))
4fE3H2E6XMp4SsxtwinF7w9a34ooUrwWe4WsW1458Pd
>>> h = 'c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6'
>>> print(encode_base58(bytes.fromhex(h)).decode('ascii'))
EQJsjkd6JaGwxrjEhfeqPenqHwrBmPQZjJGNSCHBkcF7

# end::answer4[]
# tag::exercise5[]
==== Exercise 5

Find the address corresponding to Public Keys whose Private Key secrets are:

* 5002 (use uncompressed SEC, on testnet)
* 2020^5^ (use compressed SEC, on testnet)
* 0x12345deadbeef (use compressed SEC on mainnet)
# end::exercise5[]
# tag::answer5[]
>>> from ecc import PrivateKey
>>> priv = PrivateKey(5002)
>>> print(priv.point.address(compressed=False, testnet=True))
mmTPbXQFxboEtNRkwfh6K51jvdtHLxGeMA
>>> priv = PrivateKey(2020**5)
>>> print(priv.point.address(compressed=True, testnet=True))
mopVkxp8UhXqRYbCYJsbeE1h1fiF64jcoH
>>> priv = PrivateKey(0x12345deadbeef)
>>> print(priv.point.address(compressed=True, testnet=False))
1F1Pn2y6pDb68E5nYJJeba4TLg2U7B6KF1

# end::answer5[]
# tag::exercise6[]
==== Exercise 6

Find the WIF for Private Key whose secrets are:

* 5003 (compressed, testnet)
* 2021^5^ (uncompressed, testnet)
* 0x54321deadbeef (compressed, mainnet)
# end::exercise6[]
# tag::answer6[]
>>> from ecc import PrivateKey
>>> priv = PrivateKey(5003)
>>> print(priv.wif(compressed=True, testnet=True))
cMahea7zqjxrtgAbB7LSGbcQUr1uX1ojuat9jZodMN8rFTv2sfUK
>>> priv = PrivateKey(2021**5)
>>> print(priv.wif(compressed=False, testnet=True))
91avARGdfge8E4tZfYLoxeJ5sGBdNJQH4kvjpWAxgzczjbCwxic
>>> priv = PrivateKey(0x54321deadbeef)
>>> print(priv.wif(compressed=True, testnet=False))
KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgiuQJv1h8Ytr2S53a

# end::answer6[]
# tag::exercise9[]
==== Exercise 9

Create a testnet address for yourself using a long secret that only you know. This is important as there are bots on testnet trying to steal testnet coins. Make sure you write this secret down somewhere! You will be using the secret later to sign Transactions.
# end::exercise9[]
# tag::answer9[]
>>> from ecc import PrivateKey
>>> from helper import hash256, little_endian_to_int
>>> passphrase = b'jimmy@programmingblockchain.com my secret'
>>> secret = little_endian_to_int(hash256(passphrase))
>>> priv = PrivateKey(secret)
>>> print(priv.point.address(testnet=True))
mft9LRNtaBNtpkknB8xgm17UvPedZ4ecYL

# end::answer9[]
'''


from unittest import TestCase

import helper


'''
# tag::exercise7[]
==== Exercise 7

Write a function `little_endian_to_int` which takes Python bytes, interprets those bytes in Little-Endian and returns the number.
# end::exercise7[]
'''


# tag::answer7[]
def little_endian_to_int(b):
    '''little_endian_to_int takes byte sequence as a little-endian number.
    Returns an integer'''
    return int.from_bytes(b, 'little')
# end::answer7[]


'''
# tag::exercise8[]
==== Exercise 8

Write a function `int_to_little_endian` which does the reverse of the last exercise.
# end::exercise8[]
'''


# tag::answer8[]
def int_to_little_endian(n, length):
    '''endian_to_little_endian takes an integer and returns the little-endian
    byte sequence of length'''
    return n.to_bytes(length, 'little')
# end::answer8[]


class ChapterTest(TestCase):

    def test_apply(self):
        helper.little_endian_to_int = little_endian_to_int
        helper.int_to_little_endian = int_to_little_endian
