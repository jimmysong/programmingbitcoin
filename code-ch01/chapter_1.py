from unittest import TestCase

from ecc import FieldElement


class Chapter1Test(TestCase):

    def test_apply(self):

        def ne(self, other):
            return not (self == other)

        def sub(self, other):
            if self.prime != other.prime:
                raise TypeError
            num = (self.num - other.num) % self.prime
            return self.__class__(num, self.prime)

        def mul(self, other):
            if self.prime != other.prime:
                raise TypeError
            num = self.num * other.num % self.prime
            return self.__class__(num, self.prime)

        def div(self, other):
            if self.prime != other.prime:
                raise TypeError
            num = self.num * pow(other.num, self.prime-2, self.prime) % self.prime
            return self.__class__(num, self.prime)

        FieldElement.__ne__ = ne
        FieldElement.__sub__ = sub
        FieldElement.__mul__ = mul
        FieldElement.__truediv__ = div
    
    def test_example_1(self):
        a = FieldElement(7, 13)
        b = FieldElement(6, 13)
        self.assertEqual(a == b, False)
        self.assertEqual(a == a, True)

    def test_example_2(self):
        self.assertEqual(7 % 3, 1)
        self.assertEqual(-27 % 13, 12)
        
    def test_exercise_2(self):
        prime = 57
        self.assertEqual((44 + 33) % prime, 20)
        self.assertEqual((9 - 29) % prime, 37)
        self.assertEqual((17 + 42 + 49) % prime, 51)
        self.assertEqual((52 - 30 - 38) % prime, 41)

    def test_example_3(self):
        a = FieldElement(7, 13)
        b = FieldElement(12, 13)
        c = FieldElement(6, 13)
        self.assertEqual(a + b, c)

    def test_exercise_4(self):
        prime = 97
        self.assertEqual(95 * 45 * 31 % prime, 23)
        self.assertEqual(17 * 13 * 19 * 44 % prime, 68)
        self.assertEqual(12**7 * 77**49 % prime, 63)

    def test_exercise_5(self):
        prime = 19
        for k in (1, 3, 7, 13, 18):
            self.assertEqual(
                sorted([k * i % prime for i in range(prime)]),
                [i for i in range(prime)]
            )

    def test_example_4(self):
        a = FieldElement(3, 13)
        b = FieldElement(12, 13)
        c = FieldElement(10, 13)
        self.assertEqual(a * b, c)

    def test_example_5(self):
        a = FieldElement(3, 13)
        b = FieldElement(1, 13)
        self.assertEqual(a**3, b)

    def test_exercise_7(self):
        for prime in (7, 11, 17, 31, 43):
            self.assertEqual([pow(i, prime-1, prime) for i in range(1, prime)], [1]*(prime-1))

    def test_exercise_8(self):
        prime = 31
        self.assertEqual(3 * pow(24, prime-2, prime) % prime, 4)
        self.assertEqual(pow(17, prime-4, prime), 29)
        self.assertEqual(pow(4, prime-5, prime) * 11 % prime, 13)
