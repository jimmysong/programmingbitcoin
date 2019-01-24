from unittest import TestCase, TestSuite, TextTestRunner

import hashlib


# tag::source1[]
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
# end::source1[]


def run(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)


# tag::source4[]
def hash160(s):
    '''sha256 followed by ripemd160'''
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()  # <1>
# end::source4[]


def hash256(s):
    '''two rounds of sha256'''
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


# tag::source2[]
def encode_base58(s):
    count = 0
    for c in s:  # <1>
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:  # <2>
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result  # <3>
# end::source2[]


# tag::source3[]
def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])
# end::source3[]


def decode_base58(s):
    num = 0
    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)
    combined = num.to_bytes(25, byteorder='big')
    checksum = combined[-4:]
    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError('bad address: {} {}'.format(checksum, hash256(combined[:-4])[:4]))
    return combined[1:-4]


def little_endian_to_int(b):
    '''little_endian_to_int takes byte sequence as a little-endian number.
    Returns an integer'''
    # use int.from_bytes()
    raise NotImplementedError


def int_to_little_endian(n, length):
    '''endian_to_little_endian takes an integer and returns the little-endian
    byte sequence of length'''
    # use n.to_bytes()
    raise NotImplementedError


class HelperTest(TestCase):

    def test_little_endian_to_int(self):
        h = bytes.fromhex('99c3980000000000')
        want = 10011545
        self.assertEqual(little_endian_to_int(h), want)
        h = bytes.fromhex('a135ef0100000000')
        want = 32454049
        self.assertEqual(little_endian_to_int(h), want)

    def test_int_to_little_endian(self):
        n = 1
        want = b'\x01\x00\x00\x00'
        self.assertEqual(int_to_little_endian(n, 4), want)
        n = 10011545
        want = b'\x99\xc3\x98\x00\x00\x00\x00\x00'
        self.assertEqual(int_to_little_endian(n, 8), want)
