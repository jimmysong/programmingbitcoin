from unittest import TestCase

from helper import bit_field_to_bytes, encode_varint, int_to_little_endian, murmur3


BIP37_CONSTANT = 0xfba4c795


class BloomFilter:

    def __init__(self, size, function_count, tweak):
        self.size = size
        self.bit_field = [0] * (size * 8)
        self.function_count = function_count
        self.tweak = tweak

    def add(self, item):
        '''Add an item to the filter'''
        raise NotImplementedError

    def filter_bytes(self):
        return bit_field_to_bytes(self.bit_field)

    def filterload(self, flag=1):
        '''Return the payload that goes in a filterload message'''
        raise NotImplementedError


class BloomFilterTest(TestCase):

    def test_add(self):
        bf = BloomFilter(10, 5, 99)
        item = b'Hello World'
        bf.add(item)
        expected = '0000000a080000000140'
        self.assertEqual(bf.filter_bytes().hex(), expected)
        item = b'Goodbye!'
        bf.add(item)
        expected = '4000600a080000010940'
        self.assertEqual(bf.filter_bytes().hex(), expected)

    def test_filterload(self):
        bf = BloomFilter(10, 5, 99)
        item = b'Hello World'
        bf.add(item)
        item = b'Goodbye!'
        bf.add(item)
        expected = '0a4000600a080000010940050000006300000001'
        self.assertEqual(bf.filterload().hex(), expected)
