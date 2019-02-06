'''
# tag::exercise2[]
==== Exercise 2

Solve these problems in __F__~57~ (assume all pass:[+'s] here are pass:[+<sub><em>f</em></sub>] and –'s here are pass:[–<sub><em>f</em></sub>]):

* 44 + 33
* 9 – 29
* 17 + 42 + 49
* 52 – 30 – 38
# end::exercise2[]
# tag::answer2[]
>>> prime = 57
>>> print((44+33)%prime)
20
>>> print((9-29)%prime)
37
>>> print((17+42+49)%prime)
51
>>> print((52-30-38)%prime)
41

# end::answer2[]
# tag::exercise4[]
==== Exercise 4

Solve the following equations in __F__~97~ (again, assume ⋅ and exponentiation are field pass:[<span class="keep-together">versions</span>]):

* 95 ⋅ 45 ⋅ 31
* 17 ⋅ 13 ⋅ 19 ⋅ 44
* 12^7^ ⋅ 77^49^
# end::exercise4[]
# tag::answer4[]
>>> prime = 97
>>> print(95*45*31 % prime)
23
>>> print(17*13*19*44 % prime)
68
>>> print(12**7*77**49 % prime)
63

# end::answer4[]
# tag::exercise5[]
==== Exercise 5

For _k_ = 1, 3, 7, 13, 18, what is this set in __F__~19~?

++++
<ul class="simplelist">
<li>{<em>k</em> ⋅ 0, <em>k</em> ⋅ 1, <em>k</em> ⋅ 2, <em>k</em> ⋅ 3, ... <em>k</em> ⋅ 18}</li>
</ul>
++++


Do you notice anything about these sets?
# end::exercise5[]
# tag::answer5[]
>>> prime = 19
>>> for k in (1,3,7,13,18):
...     print([k*i % prime for i in range(prime)])
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
[0, 3, 6, 9, 12, 15, 18, 2, 5, 8, 11, 14, 17, 1, 4, 7, 10, 13, 16]
[0, 7, 14, 2, 9, 16, 4, 11, 18, 6, 13, 1, 8, 15, 3, 10, 17, 5, 12]
[0, 13, 7, 1, 14, 8, 2, 15, 9, 3, 16, 10, 4, 17, 11, 5, 18, 12, 6]
[0, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
>>> for k in (1,3,7,13,18):
...     print(sorted([k*i % prime for i in range(prime)]))
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

# end::answer5[]
# tag::exercise7[]
==== Exercise 7

For _p_ = 7, 11, 17, 31, what is this set in __F~p~__?

++++
<ul class="simplelist">
<li>{1<sup>(<em>p</em> – 1)</sup>, 2<sup>(<em>p</em> – 1)</sup>, 3<sup>(<em>p</em> – 1)</sup>, 4<sup>(<em>p</em> – 1)</sup>, ... (<em>p</em> – 1)<sup>(<em>p</em> – 1)</sup>}</li>
</ul>
++++


# end::exercise7[]
# tag::answer7[]
>>> for prime in (7, 11, 17, 31):
...     print([pow(i, prime-1, prime) for i in range(1, prime)])
[1, 1, 1, 1, 1, 1]
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, \
1, 1, 1, 1, 1, 1]

# end::answer7[]
# tag::exercise8[]
==== Exercise 8

Solve the following equations in __F__~31~:

* 3 / 24
* 17^–3^
* 4^–4^ ⋅ 11
# end::exercise8[]
# tag::answer8[]
>>> prime = 31
>>> print(3*pow(24, prime-2, prime) % prime)
4
>>> print(pow(17, prime-4, prime))
29
>>> print(pow(4, prime-5, prime)*11 % prime)
13

# end::answer8[]
'''


from unittest import TestCase

from ecc import FieldElement


'''
# tag::exercise1[]
==== Exercise 1

Write the corresponding method `__ne__`, which checks if two `FieldElement` objects are _not equal_ to each other.
# end::exercise1[]
'''


# tag::answer1[]
def __ne__(self, other):
    # this should be the inverse of the == operator
    return not (self == other)
# end::answer1[]


'''
# tag::exercise3[]
==== Exercise 3

Write the corresponding `__sub__` method that defines the subtraction of two pass:[<span class="keep-together"><code>FieldElement</code></span>] objects.
# end::exercise3[]
'''


# tag::answer3[]
def __sub__(self, other):
    if self.prime != other.prime:
        raise TypeError('Cannot subtract two numbers in different Fields')
    # self.num and other.num are the actual values
    # self.prime is what we need to mod against
    num = (self.num - other.num) % self.prime
    # we return an element of the same class
    return self.__class__(num, self.prime)
# end::answer3[]


'''
# tag::exercise6[]
==== Exercise 6

Write the corresponding `__mul__` method that defines the multiplication of two finite field elements.
# end::exercise6[]
'''


# tag::answer6[]
def __mul__(self, other):
    if self.prime != other.prime:
        raise TypeError('Cannot multiply two numbers in different Fields')
    # self.num and other.num are the actual values
    # self.prime is what we need to mod against
    num = (self.num * other.num) % self.prime
    # we return an element of the same class
    return self.__class__(num, self.prime)
# end::answer6[]


'''
# tag::exercise9[]
==== Exercise 9

Write the corresponding `__truediv__` method that defines the division of two field elements.

Note that in Python 3, division is separated into `__truediv__` and `__floordiv__`. The first does normal division and the second does integer division.
# end::exercise9[]
'''


# tag::answer9[]
def __truediv__(self, other):
    if self.prime != other.prime:
        raise TypeError('Cannot divide two numbers in different Fields')
    # use Fermat's little theorem:
    # self.num**(p-1) % p == 1
    # this means:
    # 1/n == pow(n, p-2, p)
    # we return an element of the same class
    num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
    return self.__class__(num, self.prime)
# end::answer9[]


class ChapterTest(TestCase):

    def test_apply(self):
        FieldElement.__ne__ = __ne__
        FieldElement.__sub__ = __sub__
        FieldElement.__mul__ = __mul__
        FieldElement.__truediv__ = __truediv__
