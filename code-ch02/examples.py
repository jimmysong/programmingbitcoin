"""
# tag::example1[]
    >>> from ecc import Point
    >>> p1 = Point(-1, -1, 5, 7)
    >>> p2 = Point(-1, -2, 5, 7)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "ecc.py", line 143, in __init__
        raise ValueError('({}, {}) is not on the curve'.format(self.x, self.y))
    ValueError: (-1, -2) is not on the curve

# end::example1[]
# tag::example2[]
    >>> from ecc import Point
    >>> p1 = Point(-1, -1, 5, 7)
    >>> p2 = Point(-1, 1, 5, 7)
    >>> inf = Point(None, None, 5, 7)
    >>> print(p1 + inf)
    Point(-1,-1)_5_7
    >>> print(inf + p2)
    Point(-1,1)_5_7
    >>> print(p1 + p2)
    Point(infinity)

# end::example2[]
"""
