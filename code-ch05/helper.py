from unittest import TestCase, TestSuite, TextTestRunner

import hashlib


BASE58_ALPHABET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def run_test(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)


def bytes_to_str(b, encoding='ascii'):
    '''Returns a string version of the bytes'''
    return b.decode(encoding)


def str_to_bytes(s, encoding='ascii'):
    '''Returns a bytes version of the string'''
    return s.encode(encoding)


def little_endian_to_int(b):
    '''little_endian_to_int takes byte sequence as a little-endian number.
    Returns an integer'''
    # use the from_bytes method of int
    return int.from_bytes(b, 'little')


def int_to_little_endian(n, length):
    '''endian_to_little_endian takes an integer and returns the little-endian
    byte sequence of length'''
    # use the to_bytes method of n
    return n.to_bytes(length, 'little')


def hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()


def double_sha256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def encode_base58(s):
    # determine how many 0 bytes (b'\x00') s starts with
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    prefix = b'1' * count
    # convert from binary to hex, then hex to integer
    num = int(s.hex(), 16)
    result = bytearray()
    while num > 0:
        num, mod = divmod(num, 58)
        result.insert(0, BASE58_ALPHABET[mod])

    return prefix + bytes(result)


def encode_base58_checksum(s):
    return encode_base58(s + double_sha256(s)[:4]).decode('ascii')


def decode_base58(s):
    num = 0
    for c in s.encode('ascii'):
        num *= 58
        num += BASE58_ALPHABET.index(c)
    combined = num.to_bytes(25, byteorder='big')
    checksum = combined[-4:]
    if double_sha256(combined[:-4])[:4] != checksum:
        raise RuntimeError('bad address: {} {}'.format(checksum, double_sha256(combined)[:4]))
    return combined[1:-4]


def read_varint(s):
    '''read_varint reads a variable integer from a stream'''
    i = s.read(1)[0]
    if i == 0xfd:
        # 0xfd means the next two bytes are the number
        return little_endian_to_int(s.read(2))
    elif i == 0xfe:
        # 0xfe means the next four bytes are the number
        return little_endian_to_int(s.read(4))
    elif i == 0xff:
        # 0xff means the next eight bytes are the number
        return little_endian_to_int(s.read(8))
    else:
        # anything else is just the integer
        return i


def encode_varint(i):
    '''encodes an integer as a varint'''
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i, 8)
    else:
        raise RuntimeError('integer too large: {}'.format(i))


class HelperTest(TestCase):

    def test_bytes(self):
        b = b'hello world'
        s = 'hello world'
        self.assertEqual(b, str_to_bytes(s))
        self.assertEqual(s, bytes_to_str(b))

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
