'''
# tag::exercise12[]
==== Exercise 12

Calculate the new bits given the first and last blocks of this 2016 block difficulty adjustment period:

Block 471744:

```
000000203471101bbda3fe307664b3283a9ef0e97d9a38a7eacd88000000000000000000
10c8aba8479bbaa5e0848152fd3c2289ca50e1c3e58c9a4faaafbdf5803c5448ddb84559
7e8b0118e43a81d3
```

Block 473759:

```
02000020f1472d9db4b563c35f97c428ac903f23b7fc055d1cfc26000000000000000000
b3f449fcbe1bc4cfbcb8283a0d2c037f961a3fdf2b8bedc144973735eea707e126425859
7e8b0118e5f00474
```
# end::exercise12[]
# tag::answer12[]
>>> from block import Block
>>> from helper import TWO_WEEKS
>>> from helper import target_to_bits
>>> block1_hex = '000000203471101bbda3fe307664b3283a9ef0e97d9a38a7eacd8800\
000000000000000010c8aba8479bbaa5e0848152fd3c2289ca50e1c3e58c9a4faaafbdf5803c54\
48ddb845597e8b0118e43a81d3'
>>> block2_hex = '02000020f1472d9db4b563c35f97c428ac903f23b7fc055d1cfc2600\
0000000000000000b3f449fcbe1bc4cfbcb8283a0d2c037f961a3fdf2b8bedc144973735eea707\
e1264258597e8b0118e5f00474'
>>> last_block = Block.parse(BytesIO(bytes.fromhex(block1_hex)))
>>> first_block = Block.parse(BytesIO(bytes.fromhex(block2_hex)))
>>> time_differential = last_block.timestamp - first_block.timestamp
>>> if time_differential > TWO_WEEKS * 4:
...     time_differential = TWO_WEEKS * 4
>>> if time_differential < TWO_WEEKS // 4:
...     time_differential = TWO_WEEKS // 4
>>> new_target = last_block.target() * time_differential // TWO_WEEKS
>>> new_bits = target_to_bits(new_target)
>>> print(new_bits.hex())
80df6217

# end::answer12[]
'''


from io import BytesIO
from unittest import TestCase

import helper

from block import Block
from helper import (
    hash256,
    int_to_little_endian,
    little_endian_to_int,
    target_to_bits,
    TWO_WEEKS,
)
from script import Script
from tx import Tx


'''
# tag::exercise1[]
==== Exercise 1

Write the `is_coinbase` method of the `Tx` class.
# end::exercise1[]
'''

# tag::answer1[]
def is_coinbase(self):
    if len(self.tx_ins) != 1:
        return False
    first_input = self.tx_ins[0]
    if first_input.prev_tx != b'\x00' * 32:
        return False
    if first_input.prev_index != 0xffffffff:
        return False
    return True
# end::answer1[]

'''
# tag::exercise2[]
==== Exercise 2

Write the `coinbase_height` method for the `Tx` class.
# end::exercise2[]
'''

# tag::answer2[]
def coinbase_height(self):
    if not self.is_coinbase():
        return None
    element = self.tx_ins[0].script_sig.instructions[0]
    return little_endian_to_int(element)
# end::answer2[]

'''
# tag::exercise3[]
==== Exercise 3

Write the `parse` for `Block`.
# end::exercise3[]
'''

# tag::answer3[]
@classmethod
def parse(cls, s):
    version = little_endian_to_int(s.read(4))
    prev_block = s.read(32)[::-1]
    merkle_root = s.read(32)[::-1]
    timestamp = little_endian_to_int(s.read(4))
    bits = s.read(4)
    nonce = s.read(4)
    return cls(version, prev_block, merkle_root, timestamp, bits, nonce)
# end::answer3[]

'''
# tag::exercise4[]
==== Exercise 4

Write the `serialize` for `Block`.
# end::exercise4[]
'''

# tag::answer4[]
def serialize(self):
    result = int_to_little_endian(self.version, 4)
    result += self.prev_block[::-1]
    result += self.merkle_root[::-1]
    result += int_to_little_endian(self.timestamp, 4)
    result += self.bits
    result += self.nonce
    return result
# end::answer4[]

'''
# tag::exercise5[]
==== Exercise 5

Write the `hash` for `Block`.
# end::exercise5[]
'''

# tag::answer5[]
def hash(self):
    s = self.serialize()
    sha = hash256(s)
    return sha[::-1]
# end::answer5[]

'''
# tag::exercise6[]
==== Exercise 6

Write the `bip9` method for the `Block` class.
# end::exercise6[]
'''

# tag::answer6[]
def bip9(self):
    return self.version >> 29 == 0b001
# end::answer6[]

'''
# tag::exercise7[]
==== Exercise 7

Write the `bip91` method for the `Block` class.
# end::exercise7[]
'''

# tag::answer7[]
def bip91(self):
    return self.version >> 4 & 1 == 1
# end::answer7[]

'''
# tag::exercise8[]
==== Exercise 8

Write the `bip141` method for the `Block` class.
# end::exercise8[]
'''

# tag::answer8[]
def bip141(self):
    return self.version >> 1 & 1 == 1
# end::answer8[]

'''
# tag::exercise9[]
==== Exercise 9

Write the `bits_to_target` function in `helper.py`.
# end::exercise9[]
'''

# tag::answer9[]
def bits_to_target(bits):
    exponent = bits[-1]
    coefficient = little_endian_to_int(bits[:-1])
    return coefficient * 256**(exponent - 3)
# end::answer9[]

def target(self):
    return bits_to_target(self.bits)

'''
# tag::exercise10[]
==== Exercise 10

Write the `difficulty` method for `Block`
# end::exercise10[]
'''

# tag::answer10[]
def difficulty(self):
    lowest = 0xffff * 256**(0x1d - 3)
    return lowest / self.target()
# end::answer10[]

'''
# tag::exercise11[]
==== Exercise 11

Write the `check_pow` method for `Block`.

# end::exercise11[]
'''

# tag::answer11[]
def check_pow(self):
    sha = hash256(self.serialize())
    proof = little_endian_to_int(sha)
    return proof < self.target()
# end::answer11[]
'''
# tag::exercise13[]
==== Exercise 13

Write the `calculate_new_bits` function in `helper.py`
# end::exercise13[]
'''

# tag::answer13[]
def calculate_new_bits(previous_bits, time_differential):
    if time_differential > TWO_WEEKS * 4:
        time_differential = TWO_WEEKS * 4
    if time_differential < TWO_WEEKS // 4:
        time_differential = TWO_WEEKS // 4
    new_target = bits_to_target(previous_bits) * time_differential // TWO_WEEKS
    return target_to_bits(new_target)
# end::answer13[]


class ChapterTest(TestCase):

    def test_apply(self):
        Tx.is_coinbase = is_coinbase
        Tx.coinbase_height = coinbase_height
        Block.parse = parse
        Block.serialize = serialize
        Block.hash = hash
        Block.bip9 = bip9
        Block.bip91 = bip91
        Block.bip141 = bip141
        Block.difficulty = difficulty
        Block.check_pow = check_pow
        Block.target = target
        helper.calculate_new_bits = calculate_new_bits
        helper.bits_to_target = bits_to_target
