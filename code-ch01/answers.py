"""
# tag::exercise1[]
class FieldElement:
...
    def __ne__(self, other):
        # this should be the inverse of the == operator
	return not (self == other)
# end::exercise1[]
# tag::exercise2[]
    >>> prime = 57
    >>> print((44+33)%prime)
    20
    >>> print((9-29)%prime)
    37
    >>> print((17+42+49)%prime)
    51
    >>> print((52-30-38)%prime)
    41

# end::exercise2[]
# tag::exercise3[]
class FieldElement:
...
    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot subtract two numbers in different Fields')
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        num = (self.num - other.num) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)
# end::exercise3[]
# tag::exercise4[]
    >>> prime = 97
    >>> print(95*45*31 % prime)
    23
    >>> print(17*13*19*44 % prime)
    68
    >>> print(12**7*77**49 % prime)
    63

# end::exercise4[]
# tag::exercise5[]
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

# end::exercise5[]
# tag::exercise6[]
class FieldElement:
...
    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot multiply two numbers in different Fields')
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        num = (self.num * other.num) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)
# end::exercise6[]
# tag::exercise7[]
    >>> for prime in (7, 11, 17, 31):
    ...     print([pow(i, prime-1, prime) for i in range(1, prime)])
    [1, 1, 1, 1, 1, 1]
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# end::exercise7[]
# tag::exercise8[]
    >>> prime = 31
    >>> print(3*pow(24, prime-2, prime) % prime)
    4
    >>> print(pow(17, prime-4, prime))
    29
    >>> print(pow(4, prime-5, prime)*11 % prime)
    13

# end::exercise8[]
# tag::exercise9[]
class FieldElement:
...
    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot divide two numbers in different Fields')
        # use fermat's little theorem:
        # self.num**(p-1) % p == 1
        # this means:
        # 1/n == pow(n, p-2, p)
        # We return an element of the same class
	num = self.num * pow(other.num, self.prime-2, self.prime) % self.prime
	return self.__class__(num, self.prime)
# end::exercise9[]
"""
