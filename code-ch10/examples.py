'''
# tag::example1[]
>>> from io import BytesIO
>>> from network import SimpleNode, GetHeadersMessage, HeadersMessage
>>> from block import Block, GENESIS_BLOCK, LOWEST_BITS
>>> from helper import calculate_new_bits
>>> previous = Block.parse(BytesIO(GENESIS_BLOCK))
>>> first_epoch_timestamp = previous.timestamp
>>> expected_bits = LOWEST_BITS
>>> count = 1
>>> node = SimpleNode('mainnet.programmingbitcoin.com', testnet=False)
>>> node.handshake()
>>> for _ in range(19):
...     getheaders = GetHeadersMessage(start_block=previous.hash())
...     node.send(getheaders)
...     headers = node.wait_for(HeadersMessage)
...     for header in headers.blocks:
...         if not header.check_pow():  # <1>
...             raise RuntimeError('bad PoW at block {}'.format(count))
...         if header.prev_block != previous.hash():  # <2>
...             raise RuntimeError('discontinuous block at {}'.format(count))
...         if count % 2016 == 0:
...             time_diff = previous.timestamp - first_epoch_timestamp
...             expected_bits = calculate_new_bits(previous.bits, time_diff) <4>
...             print(expected_bits.hex())
...             first_epoch_timestamp = header.timestamp <5>
...         if header.bits != expected_bits:  # <3>
...             raise RuntimeError('bad bits at block {}'.format(count))
...         previous = header
...         count += 1
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
