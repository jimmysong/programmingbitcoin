'''
# tag::example1[]
>>> from io import BytesIO
>>> from script import Script
>>> stream = BytesIO(bytes.fromhex('4d04ffff001d0104455468652054696d6573203033\
2f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64\
206261696c6f757420666f722062616e6b73'))
>>> s = Script.parse(stream)
>>> print(s.cmds[2])
b'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks'

# end::example1[]
# tag::example2[]
>>> from io import BytesIO
>>> from script import Script
>>> from helper import little_endian_to_int
>>> stream = BytesIO(bytes.fromhex('5e03d71b07254d696e656420627920416e74506f6f\
6c20626a31312f4542312f4144362f43205914293101fabe6d6d678e2c8c34afc36896e7d94028\
24ed38e856676ee94bfdb0c6c4bcd8b2e5666a0400000000000000c7270000a5e00e00'))
>>> script_sig = Script.parse(stream)
>>> print(little_endian_to_int(script_sig.cmds[0]))
465879

# end::example2[]
# tag::example3[]
>>> from helper import hash256
>>> block_hash = hash256(bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7\
c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c\
3157f961db38fd8b25be1e77a759e93c0118a4ffd71d'))[::-1]
>>> block_id = block_hash.hex()
>>> print(block_id)
0000000000000000007e9e4c586439b0cdbe13b1370bdd9435d76a644d047523

# end::example3[]
# tag::example4[]
>>> from io import BytesIO
>>> from block import Block
>>> b = Block.parse(BytesIO(bytes.fromhex('020000208ec39428b17323fa0ddec8e887b\
4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3\
f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d')))
>>> print('BIP9: {}'.format(b.version >> 29 == 0b001))  # <1>
BIP9: True
>>> print('BIP91: {}'.format(b.version >> 4 & 1 == 1))  # <2>
BIP91: False
>>> print('BIP141: {}'.format(b.version >> 1 & 1 == 1))  # <3>
BIP141: True

# end::example4[]
# tag::example5[]
>>> from helper import hash256
>>> block_id = hash256(bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7c5\
3b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c31\
57f961db38fd8b25be1e77a759e93c0118a4ffd71d'))[::-1]
>>> print('{}'.format(block_id.hex()).zfill(64))  # <1>
0000000000000000007e9e4c586439b0cdbe13b1370bdd9435d76a644d047523

# end::example5[]
# tag::example6[]
>>> from helper import little_endian_to_int
>>> bits = bytes.fromhex('e93c0118')
>>> exponent = bits[-1]
>>> coefficient = little_endian_to_int(bits[:-1])
>>> target = coefficient * 256**(exponent - 3)
>>> print('{:x}'.format(target).zfill(64))  # <1>
0000000000000000013ce9000000000000000000000000000000000000000000

# end::example6[]
# tag::example7[]
>>> from helper import little_endian_to_int
>>> proof = little_endian_to_int(hash256(bytes.fromhex('020000208ec39428b17323\
fa0ddec8e887b4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d3957\
6821155e9c9e3f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d')))
>>> print(proof < target)  # <1>
True

# end::example7[]
# tag::example8[]
>>> from helper import little_endian_to_int
>>> bits = bytes.fromhex('e93c0118')
>>> exponent = bits[-1]
>>> coefficient = little_endian_to_int(bits[:-1])
>>> target = coefficient*256**(exponent-3)
>>> difficulty = 0xffff * 256**(0x1d-3) / target
>>> print(difficulty)
888171856257.3206

# end::example8[]
# tag::example9[]
>>> from block import Block
>>> from helper import TWO_WEEKS  # <1>
>>> last_block = Block.parse(BytesIO(bytes.fromhex('00000020fdf740b0e49cf75bb3\
d5168fb3586f7613dcc5cd89675b0100000000000000002e37b144c0baced07eb7e7b64da916cd\
3121f2427005551aeb0ec6a6402ac7d7f0e4235954d801187f5da9f5')))
>>> first_block = Block.parse(BytesIO(bytes.fromhex('000000201ecd89664fd205a37\
566e694269ed76e425803003628ab010000000000000000bfcade29d080d9aae8fd461254b0418\
05ae442749f2a40100440fc0e3d5868e55019345954d80118a1721b2e')))
>>> time_differential = last_block.timestamp - first_block.timestamp
>>> if time_differential > TWO_WEEKS * 4:  # <2>
...     time_differential = TWO_WEEKS * 4
>>> if time_differential < TWO_WEEKS // 4:  # <3>
...     time_differential = TWO_WEEKS // 4
>>> new_target = last_block.target() * time_differential // TWO_WEEKS
>>> print('{:x}'.format(new_target).zfill(64))
0000000000000000007615000000000000000000000000000000000000000000

# end::example9[]
'''
