'''
# tag::example1[]
>>> from helper import hash256
>>> bit_field_size = 10  # <1>
>>> bit_field = [0] * bit_field_size
>>> h = hash256(b'hello world')  # <2>
>>> bit = int.from_bytes(h, 'big') % bit_field_size  # <3>
>>> bit_field[bit] = 1  # <4>
>>> print(bit_field)
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

# end::example1[]
# tag::example2[]
>>> from helper import hash256
>>> bit_field_size = 10
>>> bit_field = [0] * bit_field_size
>>> for item in (b'hello world', b'goodbye'):  # <1>
...     h = hash256(item)
...     bit = int.from_bytes(h, 'big') % bit_field_size
...     bit_field[bit] = 1
>>> print(bit_field)
[0, 0, 1, 0, 0, 0, 0, 0, 0, 1]

# end::example2[]
# tag::example3[]
>>> from helper import hash256, hash160
>>> bit_field_size = 10
>>> bit_field = [0] * bit_field_size
>>> for item in (b'hello world', b'goodbye'):
...     for hash_function in (hash256, hash160):  # <1>
...         h = hash_function(item)
...         bit = int.from_bytes(h, 'big') % bit_field_size
...         bit_field[bit] = 1
>>> print(bit_field)
[1, 1, 1, 0, 0, 0, 0, 0, 0, 1]

# end::example3[]
# tag::example4[]
>>> from helper import murmur3  # <1>
>>> from bloomfilter import BIP37_CONSTANT  # <2>
>>> field_size = 2
>>> num_functions = 2
>>> tweak = 42
>>> bit_field_size = field_size * 8
>>> bit_field = [0] * bit_field_size
>>> for phrase in (b'hello world', b'goodbye'):  # <3>
...     for i in range(num_functions):  # <4>
...         seed = i * BIP37_CONSTANT + tweak  # <5>
...         h = murmur3(phrase, seed=seed)  # <6>
...         bit = h % bit_field_size
...         bit_field[bit] = 1
>>> print(bit_field)
[0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0]

# end::example4[]
# tag::example5[]
>>> from bloomfilter import BloomFilter
>>> from helper import decode_base58
>>> from merkleblock import MerkleBlock
>>> from network import FILTERED_BLOCK_DATA_TYPE, GetHeadersMessage, GetDataMe\
ssage, HeadersMessage, SimpleNode
>>> from tx import Tx
>>> last_block_hex = '00000000000538d5c2246336644f9a4956551afb44ba47278759ec55ea912e19'
>>> address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'
>>> h160 = decode_base58(address)
>>> node = SimpleNode('tbtc.programmingblockchain.com', testnet=True, logging=False)
>>> bf = BloomFilter(size=30, function_count=5, tweak=90210)  # <1>
>>> bf.add(h160)  # <2>
>>> node.handshake()
>>> node.send(bf.filterload())  # <3>
>>> start_block = bytes.fromhex(last_block_hex)
>>> getheaders = GetHeadersMessage(start_block=start_block)
>>> node.send(getheaders)  # <4>
>>> headers = node.wait_for(HeadersMessage)
>>> getdata = GetDataMessage()  # <5>
>>> for b in headers.blocks:
...     if not b.check_pow():
...         raise RuntimeError('proof of work is invalid')
...     getdata.add_data(FILTERED_BLOCK_DATA_TYPE, b.hash())  # <6>
>>> node.send(getdata)  # <7>
>>> found = False
>>> while not found:
...     message = node.wait_for(MerkleBlock, Tx)  # <8>
...     if message.command == b'merkleblock':
...         if not message.is_valid():  # <9>
...             raise RuntimeError('invalid merkle proof')
...     else:
...         for i, tx_out in enumerate(message.tx_outs):
...             if tx_out.script_pubkey.address(testnet=True) == address:  # <10>
...                 print('found: {}:{}'.format(message.id(), i))
...                 found = True
...                 break
found: e3930e1e566ca9b75d53b0eb9acb7607f547e1182d1d22bd4b661cfe18dcddf1:0

# end::example5[]
'''
