"""
# tag::exercise1[]
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

# end::exercise1[]
# tag::exercise2[]
class Point:
...
    def __ne__(self, other):
        # this should be the inverse of the == operator
	return not (self == other)
# end::exercise2[]
# tag::exercise3[]
class Point:
...
    def __add__(self, other):
        ...
	if self.x == other.x and self.y != other.y:
	    return self.__class__(None, None, self.a, self.b)
# end::exercise3[]
# tag::exercise4[]
    >>> x1, y1 = 2, 5
    >>> x2, y2 = -1, -1
    >>> s = (y2 - y1) / (x2 - x1)
    >>> x3 = s**2 - x1 - x2
    >>> y3 = s * (x1 - x3) - y1
    >>> print(x3, y3)
    3.0 -7.0

# end::exercise4[]
# tag::exercise5[]
class Point:
...
    def __add__(self, other):
        ...
	if self.x != other.x:
	    s = (other.y - self.y) / (other.x - self.x)
	    x3 = s**2 - self.x - other.x
	    y3 = s*(self.x - x3) - self.y
	    return self.__class__(x3, y3, self.a, self.b)
# end::exercise5[]
# tag::exercise6[]
    >>> a, x1, y1 = 5, -1, 1
    >>> s = (3 * x1**2 + a) / (2 * y1)
    >>> x3 = s**2 - 2*x1
    >>> y3 = s*(x1-x3)-y1
    >>> print(x3,y3)
    18.0 -77.0

# end::exercise6[]
# tag::exercise7[]
    def __add__(self, other):
        ...
	if self == other:
	    s = (3*self.x**2+self.a)/(2*self.y)
	    x3 = s**2 - 2*self.x
	    y3 = s*(self.x - x3) - self.y
	    return self.__class__(x3, y3, self.a, self.b)
# end::exercise7[]
"""

