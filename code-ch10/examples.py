'''
# tag::example1[]
>>> from network import SimpleNode, GetHeadersMessage, HeadersMessage
>>> from block import GENESIS_BLOCK_HASH
>>> from helper import calculate_new_bits
>>> node = SimpleNode('btc.programmingblockchain.com', testnet=False)
>>> node.handshake()
>>> last_block_hash = GENESIS_BLOCK_HASH
>>> first_epoch_block = None
>>> expected_bits = None
>>> count = 1
>>> for _ in range(19):
...     getheaders = GetHeadersMessage(start_block=last_block_hash)
...     node.send(getheaders)
...     headers = node.wait_for(HeadersMessage)
...     for b in headers.blocks:
...         if not b.check_pow():  # <1>
...             raise RuntimeError('bad proof of work at block {}'.format(count))
...         if last_block_hash != GENESIS_BLOCK_HASH and b.prev_block != last_block_hash:  # <2>
...             raise RuntimeError('discontinuous block at {}'.format(count))
...         if expected_bits and b.bits != expected_bits:  # <3>
...             raise RuntimeError('bad bits at block {}'.format(count))
...         if first_epoch_block and count % 2016 == 2015:  # <4>
...             expected_bits = calculate_new_bits(
...                 expected_bits, b.timestamp - first_epoch_block.timestamp)
...             print(expected_bits.hex())
...         elif first_epoch_block is None:  # <5>
...             expected_bits = b.bits
...         if count % 2016 == 0 or not first_epoch_block:
...             first_epoch_block = b
...         count += 1
...         last_block_hash = b.hash()
ffff001d
ffff001d
ffff001d
ffff001d
ffff001d
ffff001d
ffff001d
ffff001d
ffff001d
ffff001d
ffff001d
ffff001d
ffff001d
ffff001d
ffff001d
6ad8001d
28c4001d
71be001d

# end::example1[]
'''
