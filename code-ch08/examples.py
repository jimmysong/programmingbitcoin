'''
# tag::example1[]
>>> from helper import encode_base58_checksum
>>> h160 = bytes.fromhex('74d691da1574e6b3c192ecfb52cc8984ee7b6c56')
>>> print(encode_base58_checksum(b'\x05' + h160))
3CLoMMyuoDQTPRD3XYZtCvgvkadrAdvdXh

# end::example1[]
# tag::example2[]
>>> from helper import hash256
>>> modified_tx = bytes.fromhex('0100000001868278ed6ddfb6c1ed3ad5f8181eb0c7a38\
5aa0836f01d5e4789e6bd304d87221a000000475221022626e955ea6ea6d98850c994f9107b036\
b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98be\
c453e1ffac7fbdbd4bb7152aeffffffff04d3b11400000000001976a914904a49878c0adfc3aa0\
5de7afad2cc15f483a56a88ac7f400900000000001976a914418327e3f3dda4cf5b9089325a4b9\
5abdfa0334088ac722c0c00000000001976a914ba35042cfe9fc66fd35ac2224eebdafd1028ad2\
788acdc4ace020000000017a91474d691da1574e6b3c192ecfb52cc8984ee7b6c5687000000000\
1000000')
>>> s256 = hash256(modified_tx)
>>> z = int.from_bytes(s256, 'big')
>>> print(hex(z))
0xe71bfa115715d6fd33796948126f40a8cdd39f187e4afb03896795189fe1423c

# end::example2[]
# tag::example3[]
>>> from ecc import S256Point, Signature
>>> from helper import hash256
>>> modified_tx = bytes.fromhex('0100000001868278ed6ddfb6c1ed3ad5f8181eb0c7a38\
5aa0836f01d5e4789e6bd304d87221a000000475221022626e955ea6ea6d98850c994f9107b036\
b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98be\
c453e1ffac7fbdbd4bb7152aeffffffff04d3b11400000000001976a914904a49878c0adfc3aa0\
5de7afad2cc15f483a56a88ac7f400900000000001976a914418327e3f3dda4cf5b9089325a4b9\
5abdfa0334088ac722c0c00000000001976a914ba35042cfe9fc66fd35ac2224eebdafd1028ad2\
788acdc4ace020000000017a91474d691da1574e6b3c192ecfb52cc8984ee7b6c5687000000000\
1000000')
>>> h256 = hash256(modified_tx)
>>> z = int.from_bytes(h256, 'big')  # <1>
>>> sec = bytes.fromhex('022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff\
1295d21cfdb70')
>>> der = bytes.fromhex('3045022100dc92655fe37036f47756db8102e0d7d5e28b3beb83a\
8fef4f5dc0559bddfb94e02205a36d4e4e6c7fcd16658c50783e00c341609977aed3ad00937bf4\
ee942a89937')
>>> point = S256Point.parse(sec)
>>> sig = Signature.parse(der)
>>> print(point.verify(z, sig))
True

# end::example3[]
'''
