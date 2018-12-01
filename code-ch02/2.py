from unittest import TestCase

from ecc import Point


def ne(self, other):
    return not (self == other)

def add(self, other):
    if self.a != other.a or self.b != other.b:
        raise TypeError
    if self.x is None:
        return other
    if other.x is None:
        return self
    if self.x == other.x and self.y != other.y:
        return self.__class__(None, None, self.a, self.b)
    if self.x != other.x:
        s = (other.y - self.y) / (other.x - self.x)
        x = s**2 - self.x - other.x
        y = s * (self.x - x) - self.y
        return self.__class__(x, y, self.a, self.b)
    if self == other and self.y == 0 * self.x:
        return self.__class__(None, None, self.a, self.b)
    if self == other:
        s = (3 * self.x**2 + self.a) / (2 * self.y)
        x = s**2 - 2 * self.x
        y = s * (self.x - x) - self.y
        return self.__class__(x, y, self.a, self.b)


class Chapter2Test(TestCase):

    def test_apply(self):
        Point.__ne__ = ne
        Point.__add__ = add
