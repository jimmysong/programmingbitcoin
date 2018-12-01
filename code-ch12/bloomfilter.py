from unittest import TestCase

from helper import (
    bit_field_to_bytes,
    encode_varint,
    int_to_little_endian,
    murmur3,
)
from network import GenericMessage


BIP37_CONSTANT = 0xfba4c795


class BloomFilter:

    def __init__(self, size, function_count, tweak):
        self.size = size
        self.bit_field = [0] * (size * 8)
        self.function_count = function_count
        self.tweak = tweak

    def add(self, item):
        '''Add an item to the filter'''
        # iterate self.function_count number of times
            # BIP0037 spec seed is i*BIP37_CONSTANT + self.tweak
            # get the murmur3 hash given that seed
            # set the bit at the hash mod the bitfield size (self.size*8)
            # set the bit field at bit to be 1
        raise NotImplementedError

    def filter_bytes(self):
        return bit_field_to_bytes(self.bit_field)

    def filterload(self, flag=1):
        '''Return the filterload message'''
        # start the payload with the size of the filter in bytes
        # next add the bit field using self.filter_bytes()
        # function count is 4 bytes little endian
        # tweak is 4 bytes little endian
        # flag is 1 byte little endian
        # return a GenericMessage whose command is b'filterload'
        # and payload is what we've calculated
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
        self.assertEqual(bf.filterload().serialize().hex(), expected)
