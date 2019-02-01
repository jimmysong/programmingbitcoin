'''
# tag::exercise1[]
==== Exercise 1

Calculate the Bloom Filter for "hello world" and "goodbye" using the hash160 hash function over a bit field of 10.
# end::exercise1[]
# tag::answer1[]
>>> from helper import hash160
>>> bit_field_size = 10
>>> bit_field = [0] * bit_field_size
>>> for item in (b'hello world', b'goodbye'):
...     h = hash160(item)
...     bit = int.from_bytes(h, 'big') % bit_field_size
...     bit_field[bit] = 1
>>> print(bit_field)
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

# end::answer1[]
# tag::exercise2[]
==== Exercise 2

Given a Bloom Filter with `size=10`, `function_count=5`, `tweak=99`, what are the bytes that are set after adding these items? (Use `bit_field_to_bytes` to convert to bytes.)

* `b'Hello World'`
* `b'Goodbye!'`
# end::exercise2[]
# tag::answer2[]
>>> from bloomfilter import BloomFilter, BIP37_CONSTANT
>>> from helper import bit_field_to_bytes, murmur3
>>> field_size = 10
>>> function_count = 5
>>> tweak = 99
>>> items = (b'Hello World',  b'Goodbye!')
>>> bit_field_size = field_size * 8
>>> bit_field = [0] * bit_field_size
>>> for item in items:
...     for i in range(function_count):
...         seed = i * BIP37_CONSTANT + tweak
...         h = murmur3(item, seed=seed)
...         bit = h % bit_field_size
...         bit_field[bit] = 1
>>> print(bit_field_to_bytes(bit_field).hex())
4000600a080000010940

# end::answer2[]
# tag::exercise6[]
==== Exercise 6

Get the current testnet block ID, send yourself some testnet coins, find the UTXO corresponding to the testnet coin _without using a block explorer_, create a transaction using that UTXO as an input, and broadcast the `tx` message on the  testnet network.
# end::exercise6[]
# tag::answer6[]
>>> import time
>>> from block import Block
>>> from bloomfilter import BloomFilter
>>> from ecc import PrivateKey
>>> from helper import (
...     decode_base58,
...     encode_varint,
...     hash256,
...     little_endian_to_int,
...     read_varint,
... )
>>> from merkleblock import MerkleBlock
>>> from network import (
...     GetDataMessage,
...     GetHeadersMessage,
...     HeadersMessage,
...     NetworkEnvelope,
...     SimpleNode,
...     TX_DATA_TYPE,
...     FILTERED_BLOCK_DATA_TYPE,
... )
>>> from script import p2pkh_script, Script
>>> from tx import Tx, TxIn, TxOut
>>> last_block_hex = '00000000000000a03f9432ac63813c6710bfe41712ac5ef6faab093f\
e2917636'
>>> secret = little_endian_to_int(hash256(b'Jimmy Song'))
>>> private_key = PrivateKey(secret=secret)
>>> addr = private_key.point.address(testnet=True)
>>> h160 = decode_base58(addr)
>>> target_address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'
>>> target_h160 = decode_base58(target_address)
>>> target_script = p2pkh_script(target_h160)
>>> fee = 5000  # fee in satoshis
>>> # connect to testnet.programmingbitcoin.com in testnet mode
>>> node = SimpleNode('testnet.programmingbitcoin.com', testnet=True, logging=\
False)
>>> # create a bloom filter of size 30 and 5 functions. Add a tweak.
>>> bf = BloomFilter(30, 5, 90210)
>>> # add the h160 to the bloom filter
>>> bf.add(h160)
>>> # complete the handshake
>>> node.handshake()
>>> # load the bloom filter with the filterload command
>>> node.send(bf.filterload())
>>> # set start block to last_block from above
>>> start_block = bytes.fromhex(last_block_hex)
>>> # send a getheaders message with the starting block
>>> getheaders = GetHeadersMessage(start_block=start_block)
>>> node.send(getheaders)
>>> # wait for the headers message
>>> headers = node.wait_for(HeadersMessage)
>>> # store the last block as None
>>> last_block = None
>>> # initialize the GetDataMessage
>>> getdata = GetDataMessage()
>>> # loop through the blocks in the headers
>>> for b in headers.blocks:
...     # check that the proof of work on the block is valid
...     if not b.check_pow():
...         raise RuntimeError('proof of work is invalid')
...     # check that this block's prev_block is the last block
...     if last_block is not None and b.prev_block != last_block:
...         raise RuntimeError('chain broken')
...     # add a new item to the getdata message
...     # should be FILTERED_BLOCK_DATA_TYPE and block hash
...     getdata.add_data(FILTERED_BLOCK_DATA_TYPE, b.hash())
...     # set the last block to the current hash
...     last_block = b.hash()
>>> # send the getdata message
>>> node.send(getdata)
>>> # initialize prev_tx, prev_index and prev_amount to None
>>> prev_tx, prev_index, prev_amount = None, None, None
>>> # loop while prev_tx is None
>>> while prev_tx is None:
...     # wait for the merkleblock or tx commands
...     message = node.wait_for(MerkleBlock, Tx)
...     # if we have the merkleblock command
...     if message.command == b'merkleblock':
...         # check that the MerkleBlock is valid
...         if not message.is_valid():
...             raise RuntimeError('invalid merkle proof')
...     # else we have the tx command
...     else:
...         # set the tx's testnet to be True
...         message.testnet = True
...         # loop through the tx outs
...         for i, tx_out in enumerate(message.tx_outs):
...             # if our output has the same address as our address we found it
...             if tx_out.script_pubkey.address(testnet=True) == addr:
...                 # we found our utxo. set prev_tx, prev_index, and tx
...                 prev_tx = message.hash()
...                 prev_index = i
...                 prev_amount = tx_out.amount
...                 print('found: {}:{}'.format(prev_tx.hex(), prev_index))
found: b2cddd41d18d00910f88c31aa58c6816a190b8fc30fe7c665e1cd2ec60efdf3f:7
>>> # create the TxIn
>>> tx_in = TxIn(prev_tx, prev_index)
>>> # calculate the output amount (previous amount minus the fee)
>>> output_amount = prev_amount - fee
>>> # create a new TxOut to the target script with the output amount
>>> tx_out = TxOut(output_amount, target_script)
>>> # create a new transaction with the one input and one output
>>> tx_obj = Tx(1, [tx_in], [tx_out], 0, testnet=True)
>>> # sign the only input of the transaction
>>> print(tx_obj.sign_input(0, private_key))
True
>>> # serialize and hex to see what it looks like
>>> print(tx_obj.serialize().hex())
01000000013fdfef60ecd21c5e667cfe30fcb890a116688ca51ac3880f91008dd141ddcdb20700\
00006b483045022100ff77d2559261df5490ed00d231099c4b8ea867e6ccfe8e3e6d077313ed4f\
1428022033a1db8d69eb0dc376f89684d1ed1be75719888090388a16f1e8eedeb8067768012103\
dc585d46cfca73f3a75ba1ef0c5756a21c1924587480700c6eb64e3f75d22083ffffffff019334\
e500000000001976a914ad346f8eb57dee9a37981716e498120ae80e44f788ac00000000
>>> # send this signed transaction on the network
>>> node.send(tx_obj)
>>> # wait a sec so this message goes through with time.sleep(1)
>>> time.sleep(1)
>>> # now ask for this transaction from the other node
>>> # create a GetDataMessage
>>> getdata = GetDataMessage()
>>> # ask for our transaction by adding it to the message
>>> getdata.add_data(TX_DATA_TYPE, tx_obj.hash())
>>> # send the message
>>> node.send(getdata)
>>> # now wait for a Tx response
>>> received_tx = node.wait_for(Tx)
>>> # if the received tx has the same id as our tx, we are done!
>>> if received_tx.id() == tx_obj.id():
...     print('success!')
success!

# end::answer6[]
'''


from unittest import TestCase

from bloomfilter import BloomFilter, BIP37_CONSTANT
from helper import (
    encode_varint,
    int_to_little_endian,
    murmur3,
)
from network import (
    GenericMessage,
    GetDataMessage,
)


'''
# tag::exercise3[]
==== Exercise 3

Write the `add` method for `BloomFilter`.
# end::exercise3[]
'''


# tag::answer3[]
def add(self, item):
    for i in range(self.function_count):
        seed = i * BIP37_CONSTANT + self.tweak
        h = murmur3(item, seed=seed)
        bit = h % (self.size * 8)
        self.bit_field[bit] = 1
# end::answer3[]


'''
# tag::exercise4[]
==== Exercise 4

Write the  `filterload` method for the `BloomFilter` class.
# end::exercise4[]
'''


# tag::answer4[]
def filterload(self, flag=1):
    payload = encode_varint(self.size)
    payload += self.filter_bytes()
    payload += int_to_little_endian(self.function_count, 4)
    payload += int_to_little_endian(self.tweak, 4)
    payload += int_to_little_endian(flag, 1)
    return GenericMessage(b'filterload', payload)
# end::answer4[]


'''
# tag::exercise5[]
==== Exercise 5

Write the `serialize` method for the `GetDataMessage` class.
# end::exercise5[]
'''


# tag::answer5[]
def serialize(self):
    result = encode_varint(len(self.data))
    for data_type, identifier in self.data:
        result += int_to_little_endian(data_type, 4)
        result += identifier[::-1]
    return result
# end::answer5[]


class ChapterTest(TestCase):

    def test_apply(self):
        BloomFilter.add = add
        BloomFilter.filterload = filterload
        GetDataMessage.serialize = serialize
