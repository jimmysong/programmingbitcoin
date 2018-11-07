from unittest import TestCase

from ecc import FieldElement, Point, S256Point, ECCTest, G, N
from random import randint
from helper import hash256


class Chapter2Test(TestCase):

    def test_apply(self):

        def test_add(self):
            prime = 223
            a = FieldElement(0, prime)
            b = FieldElement(7, prime)
            additions = (
                (192, 105, 17, 56, 170, 142),
                (47, 71, 117, 141, 60, 139),
                (143, 98, 76, 66, 47, 71),
            )
            for x1_raw, y1_raw, x2_raw, y2_raw, x3_raw, y3_raw in additions:
                x1 = FieldElement(x1_raw, prime)
                y1 = FieldElement(y1_raw, prime)
                p1 = Point(x1, y1, a, b)
                x2 = FieldElement(x2_raw, prime)
                y2 = FieldElement(y2_raw, prime)
                p2 = Point(x2, y2, a, b)
                x3 = FieldElement(x3_raw, prime)
                y3 = FieldElement(y3_raw, prime)
                p3 = Point(x3, y3, a, b)
                self.assertEqual(p1 + p2, p3)

        ECCTest.test_add = test_add

    def test_exercise_1(self):

        def on_curve(x,y):
            return y**2 == x**3 + a*x + b

        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        self.assertEqual(on_curve(FieldElement(192, prime), FieldElement(105, prime)), True)
        self.assertEqual(on_curve(FieldElement(17, prime), FieldElement(56, prime)), True)
        self.assertEqual(on_curve(FieldElement(200, prime), FieldElement(119, prime)), False)
        self.assertEqual(on_curve(FieldElement(1, prime), FieldElement(193, prime)), True)
        self.assertEqual(on_curve(FieldElement(42, prime), FieldElement(99, prime)), False)

    def test_example_1(self):
        a = FieldElement(num=0, prime=223)
        b = FieldElement(num=7, prime=223)
        x = FieldElement(num=192, prime=223)
        y = FieldElement(num=105, prime=223)
        p1 = Point(x, y, a, b)
        self.assertEqual(p1.x.num, 192)
        self.assertEqual(p1.y.num, 105)
        self.assertEqual(p1.x.prime, 223)

    def test_example_3(self):
        prime = 223
        a = FieldElement(num=0, prime=prime)
        b = FieldElement(num=7, prime=prime)
        x1 = FieldElement(num=192, prime=prime)
        y1 = FieldElement(num=105, prime=prime)
        x2 = FieldElement(num=17, prime=prime)
        y2 = FieldElement(num=56, prime=prime)
        p1 = Point(x1, y1, a, b)
        p2 = Point(x2, y2, a, b)
        p3 = p1 + p2
        self.assertEqual(p3.x.num, 170)
        self.assertEqual(p3.y.num, 142)
        self.assertEqual(p3.x.prime, 223)

    def test_exercise_2(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        p1 = Point(FieldElement(170, prime), FieldElement(142, prime), a, b)
        p2 = Point(FieldElement(60, prime), FieldElement(139, prime), a, b)
        p3 = p1 + p2
        self.assertEqual(p3.x.num, 220)
        self.assertEqual(p3.y.num, 181)
        self.assertEqual(p3.x.prime, prime)
        p1 = Point(FieldElement(47, prime), FieldElement(71, prime), a, b)
        p2 = Point(FieldElement(17, prime), FieldElement(56, prime), a, b)
        p3 = p1 + p2
        self.assertEqual(p3.x.num, 215)
        self.assertEqual(p3.y.num, 68)
        self.assertEqual(p3.x.prime, prime)
        p1 = Point(FieldElement(143, prime), FieldElement(98, prime), a, b)
        p2 = Point(FieldElement(76, prime), FieldElement(66, prime), a, b)
        p3 = p1 + p2
        self.assertEqual(p3.x.num, 47)
        self.assertEqual(p3.y.num, 71)
        self.assertEqual(p3.x.prime, prime)

    def test_exercise_4(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x1 = FieldElement(num=192, prime=prime)
        y1 = FieldElement(num=105, prime=prime)
        p = Point(x1,y1,a,b)
        p2 = p + p
        self.assertEqual(p2.x.num, 49)
        self.assertEqual(p2.y.num, 71)
        self.assertEqual(p2.x.prime, prime)
        x1 = FieldElement(num=143, prime=prime)
        y1 = FieldElement(num=98, prime=prime)
        p = Point(x1,y1,a,b)
        p2 = p + p
        self.assertEqual(p2.x.num, 64)
        self.assertEqual(p2.y.num, 168)
        self.assertEqual(p2.x.prime, prime)
        x1 = FieldElement(num=47, prime=prime)
        y1 = FieldElement(num=71, prime=prime)
        p = Point(x1,y1,a,b)
        p2 = p + p
        self.assertEqual(p2.x.num, 36)
        self.assertEqual(p2.y.num, 111)
        self.assertEqual(p2.x.prime, prime)
        p2 = p + p + p + p
        self.assertEqual(p2.x.num, 194)
        self.assertEqual(p2.y.num, 51)
        self.assertEqual(p2.x.prime, prime)
        p2 = p+p+p+p+p+p+p+p
        self.assertEqual(p2.x.num, 116)
        self.assertEqual(p2.y.num, 55)
        self.assertEqual(p2.x.prime, prime)
        p2 = p+p+p+p+p+p+p+p+p+p+p+p+p+p+p+p+p+p+p+p+p
        self.assertEqual(p2.x, None)

    def test_example_4(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(47, prime)
        y = FieldElement(71, prime)
        p = Point(x, y, a, b)
        want = (
            (None, None),
            (47,71),
            (36,111),
            (15,137),
            (194,51),
            (126,96),
            (139,137),
            (92,47),
            (116,55),
            (69,86),
            (154,150),
            (154,73),
            (69,137),
            (116,168),
            (92,176),
            (139,86),
            (126,127),
            (194,172),
            (15,86),
            (36,112),
            (47,152),
        )
        for s in range(1, 21):
            result = s*p
            self.assertEqual((result.x.num, result.y.num), want[s])

    def test_exercise_5(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(15, prime)
        y = FieldElement(86, prime)
        p = Point(x, y, a, b)
        inf = Point(None, None, a, b)
        product = p
        count = 1
        while product != inf:
            product += p
            count += 1
        self.assertEqual(count, 7)

    def test_example_5(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(15, prime)
        y = FieldElement(86, prime)
        p = Point(x, y, a, b)
        p2 = 7*p
        self.assertEqual(p2.x, None)

    def test_example_6(self):
        gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
        gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        p = 2**256 - 2**32 - 977
        self.assertEqual(gy**2 % p == (gx**3 + 7) % p, True)

    def test_example_7(self):
        gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
        gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        p = 2**256 - 2**32 - 977
        n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
        x = FieldElement(gx, p)
        y = FieldElement(gy, p)
        seven = FieldElement(7, p)
        zero = FieldElement(0, p)
        G = Point(x, y, zero, seven)
        p2 = n*G
        self.assertEqual(p2.x, None)

    def test_example_8(self):
        p = N*G
        self.assertEqual(p.x, None)

    def test_example_9(self):
        z = 0xbc62d4b80d9e36da29c16c5d4d9f11731f36052c72401a76c23c0fb5a9b74423
        r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
        s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        point = S256Point(0x04519fac3d910ca7e7138f7013706f619fa8f033e6ec6e09370ea38cee6a7574, 0x82b51eab8c27c66e26c858a079bcdf4f1ada34cec420cafc7eac1a42216fb6c4)
        u = z * pow(s, N-2, N) % N
        v = r * pow(s, N-2, N) % N
        self.assertEqual((u*G + v*point).x.num, r)

    def test_exercise_6(self):
        point = S256Point(
            0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c, 
            0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34)
        z = 0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60
        r = 0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395
        s = 0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4
        u = z * pow(s, N-2, N) % N
        v = r * pow(s, N-2, N) % N
        self.assertEqual((u*G + v*point).x.num, r)
        z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
        r = 0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c
        s = 0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6
        u = z * pow(s, N-2, N) % N
        v = r * pow(s, N-2, N) % N
        self.assertEqual((u*G + v*point).x.num, r)

    def test_example_10(self):
        e = int.from_bytes(hash256(b'my secret'), 'big')
        z = int.from_bytes(hash256(b'my message'), 'big')
        k = randint(0, N)
        r = (k*G).x.num
        k_inv = pow(k, N-2, N)
        s = (z+r*e) * k_inv % N
        point = e*G
        self.assertEqual(
            point.x.num,
            0x028d003eab2e428d11983f3e97c3fa0addf3b42740df0d211795ffb3be2f6c52)
        self.assertEqual(
            point.y.num,
            0x0ae987b9ec6ea159c78cb2a937ed89096fb218d9e7594f02b547526d8cd309e2)
        self.assertEqual(
            z,
            0x231c6f3d980a6b0fb7152f85cee7eb52bf92433d9919b9c5218cb08e79cce78)

    def test_exercise_7(self):
        e = 12345
        z = int.from_bytes(hash256(b'Programming Bitcoin!'), 'big')
        k = randint(0, N)
        r = (k*G).x.num
        k_inv = pow(k, N-2, N)
        s = (z+r*e) * k_inv % N
        point = e*G
        self.assertEqual(
            point.x.num,
            0xf01d6b9018ab421dd410404cb869072065522bf85734008f105cf385a023a80f)
        self.assertEqual(
            point.y.num,
            0x0eba29d0f0c5408ed681984dc525982abefccd9f7ff01dd26da4999cf3f6a295)
        self.assertEqual(
            z,
            0x969f6056aa26f7d2795fd013fe88868d09c9f6aed96965016e1936ae47060d48)
