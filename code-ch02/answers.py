from unittest import TestCase

from ecc import Point


'''
# tag::exercise2[]
==== Exercise 2

Write the `__ne__` method for `Point`.
# end::exercise2[]
'''

# tag::answer2[]
def __ne__(self, other):
    return not (self == other)
# end::answer2[]

'''
# tag::exercise3[]
==== Exercise 3

Handle the case where the two points are additive inverses. That is, they have the same `x`, but a different `y`, causing a vertical line. This should return the point at infinity.
# end::exercise3[]
# tag::exercise5[]
==== Exercise 5

Write the `__add__` method where x~1~≠x~2~
# end::exercise5[]
# tag::exercise7[]
==== Exercise 7

Write the `__add__` method when P~1~=P~2~.
# end::exercise7[]
'''

def __add__(self, other):
    if self.a != other.a or self.b != other.b:
        raise TypeError
    if self.x is None:
        return other
    if other.x is None:
        return self
    # tag::answer3[]
    if self.x == other.x and self.y != other.y:
        return self.__class__(None, None, self.a, self.b)
    # end::answer3[]
    # tag::answer5[]
    if self.x != other.x:
        s = (other.y - self.y) / (other.x - self.x)
        x = s**2 - self.x - other.x
        y = s * (self.x - x) - self.y
        return self.__class__(x, y, self.a, self.b)
    # end::answer5[]
    if self == other and self.y == 0 * self.x:
        return self.__class__(None, None, self.a, self.b)
    # tag::answer7[]
    if self == other:
        s = (3 * self.x**2 + self.a) / (2 * self.y)
        x = s**2 - 2 * self.x
        y = s * (self.x - x) - self.y
        return self.__class__(x, y, self.a, self.b)
    # tag::answer7[]


class DocTest:
    '''
    # tag::exercise1[]
    ==== Exercise 1

    Determine which of these points are on the curve y^2^=x^3^+5x+7:

    (2,4), (-1,-1), (18,77), (5,7)
    # end::exercise1[]
    # tag::answer1[]
    >>> def on_curve(x, y):
    ...     return y**2 == x**3 + 5*x + 7
    >>> print(on_curve(2,4))
    False
    >>> print(on_curve(-1,-1))
    True
    >>> print(on_curve(18,77))
    True
    >>> print(on_curve(5,7))
    False

    # end::answer1[]
    # tag::exercise4[]
    ==== Exercise 4

    For the curve y^2^=x^3^+5x+7, what is (2,5) + (-1,-1)?
    # end::exercise4[]
    # tag::answer4[]
    >>> x1, y1 = 2, 5
    >>> x2, y2 = -1, -1
    >>> s = (y2 - y1) / (x2 - x1)
    >>> x3 = s**2 - x1 - x2
    >>> y3 = s * (x1 - x3) - y1
    >>> print(x3, y3)
    3.0 -7.0

    # end::answer4[]
    # tag::exercise6[]
    ==== Exercise 6

    For the curve y^2^=x^3^+5x+7, what is (2,5) + (-1,-1)?
    # end::exercise6[]
    # tag::answer6[]
    >>> a, x1, y1 = 5, -1, 1
    >>> s = (3 * x1**2 + a) / (2 * y1)
    >>> x3 = s**2 - 2*x1
    >>> y3 = s*(x1-x3)-y1
    >>> print(x3,y3)
    18.0 -77.0

    # end::answer6[]
    '''


class ChapterTest(TestCase):

    def test_apply(self):
        Point.__ne__ = __ne__
        Point.__add__ = __add__
