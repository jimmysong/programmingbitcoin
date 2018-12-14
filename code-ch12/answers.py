from unittest import TestCase

from bloomfilter import BloomFilter, BIP37_CONSTANT
from ecc import PrivateKey
from helper import (
    bit_field_to_bytes,
    decode_base58,
    encode_varint,
    hash160,
    hash256,
    int_to_little_endian,
    little_endian_to_int,
    murmur3,
)
from merkleblock import MerkleBlock
from network import (
    GenericMessage,
    GetDataMessage,
    GetHeadersMessage,
    HeadersMessage,
    SimpleNode,
    FILTERED_BLOCK_DATA_TYPE,
)
from script import p2pkh_script, Script
from tx import Tx, TxIn, TxOut, TxFetcher


'''
# tag::exercise3[]
==== Exercise 3

Write the `add` method for `BloomFilter`
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

Write the  `filterload` payload from the `BloomFilter` class.
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


class DocTest:
    '''
    # tag::exercise1[]
    ==== Exercise 1

    Calculate the Bloom Filter for 'hello world' and 'goodbye' using the `hash160` hash function over a bit field of 10.
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

    Given a Bloom Filter with size=10, function count=5, tweak=99, what are the bytes that are set after adding these items? (use `bit_field_to_bytes` to convert to bytes)

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

    Get the current testnet block ID, send yourself some testnet coins, find the UTXO corresponding to the testnet coin _without using a block explorer_, create a transaction using that UTXO as an input and broadcast the `tx` message on the  testnet network.
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
    ...     SIGHASH_ALL,
    >>> )
    >>> from merkleblock import MerkleBlock
    >>> from network import (
    ...     GetDataMessage,
    ...     GetHeadersMessage,
    ...     HeadersMessage,
    ...     NetworkEnvelope,
    ...     SimpleNode,
    ...     TX_DATA_TYPE,
    ...     FILTERED_BLOCK_DATA_TYPE,
    >>> )
    >>> from script import p2pkh_script, Script
    >>> from tx import Tx, TxIn, TxOut, TxFetcher
    >>> last_block_hex = '00000000000538d5c2246336644f9a4956551afb44ba47278759ec55ea912e19'
    >>> secret = little_endian_to_int(hash256(b''))
    >>> private_key = PrivateKey(secret=secret)
    >>> addr = private_key.point.address(testnet=True)
    >>> h160 = decode_base58(addr)
    >>> target_address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'
    >>> target_h160 = decode_base58(target_address)
    >>> target_script = p2pkh_script(target_h160)
    >>> fee = 5000  # fee in satoshis
    >>> node = SimpleNode('tbtc.programmingblockchain.com', testnet=True, logging=True)
    >>> bf = BloomFilter(30, 5, 90210)
    >>> bf.add(h160)
    >>> node.handshake()
    >>> node.send(bf.filterload())
    >>> start_block = bytes.fromhex(last_block_hex)
    >>> getheaders = GetHeadersMessage(start_block=start_block)
    >>> node.send(getheaders)
    >>> headers = node.wait_for(HeadersMessage)
    >>> last_block = None
    >>> getdata = GetDataMessage()
    >>> for b in headers.blocks:
    ...     if not b.check_pow():
    ...         raise RuntimeError('proof of work is invalid')
    ...     if last_block is not None and b.prev_block != last_block:
    ...         raise RuntimeError('chain broken')
    ...     getdata.add_data(FILTERED_BLOCK_DATA_TYPE, b.hash())
    ...     last_block = b.hash()
    >>> node.send(getdata)
    >>> prev_tx, prev_index = None, None
    >>> while prev_tx is None:
    ...     message = node.wait_for(MerkleBlock, Tx)
    ...     if message.command == b'merkleblock':
    ...         if not message.is_valid():
    ...             raise RuntimeError('invalid merkle proof')
    ...     else:
    ...         message.testnet = True
    ...         for i, tx_out in enumerate(message.tx_outs):
    ...             if tx_out.script_pubkey.address(testnet=True) == addr:
    ...                 prev_tx = message.hash()
    ...                 prev_index = i
    ...                 print('found: {}:{}'.format(prev_tx.hex(), prev_index))
    >>> tx_in = TxIn(prev_tx, prev_index)
    >>> output_amount = prev_amount - fee
    >>> tx_outs = TxOut(output_amount, target_script)
    >>> tx_obj = Tx(1, [tx_in], [tx_out], 0, testnet=True)
    >>> tx_obj.sign_input(0, private_key)
    >>> print(tx_obj.serialize().hex())
    010000000194e631abb9e1079ec72a1616a3aa0111c614e65b96a6a4420e2cc6af9e6cc96e\
000000006a47304402203cc8c56abe1c0dd043afa9eb125dafbebdde2dd4cd7abf0fb1aae0667a\
22006e02203c95b74d0f0735bbf1b261d36e077515b6939fc088b9d7c1b7030a5e494596330121\
021cdd761c7eb1c90c0af0a5963e94bf0203176b4662778d32bd6d7ab5d8628b32ffffffff01f8\
829800000000001976a914ad346f8eb57dee9a37981716e498120ae80e44f788ac00000000
    >>> node.send(tx_obj)
    >>> time.sleep(1)
    >>> getdata = GetDataMessage()
    >>> getdata.add_data(TX_DATA_TYPE, tx_obj.hash())
    >>> node.send(getdata)
    >>> received_tx = node.wait_for(Tx)
    >>> if received_tx.id() == tx_obj.id():
    ...     print('success!')
    success!

    # end::answer6[]
    '''

class ChapterTest(TestCase):

    def test_apply(self):
        BloomFilter.add = add
        BloomFilter.filterload = filterload
        GetDataMessage.serialize = serialize
