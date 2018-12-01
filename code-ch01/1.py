from unittest import TestCase

from ecc import FieldElement


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
    num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
    return self.__class__(num, self.prime)


class Chapter1Test(TestCase):

    def test_apply(self):
        FieldElement.__ne__ = ne
        FieldElement.__sub__ = sub
        FieldElement.__mul__ = mul
        FieldElement.__truediv__ = div
