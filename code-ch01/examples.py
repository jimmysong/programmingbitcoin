"""
# tag::example1[]
    >>> from ecc import FieldElement
    >>> a = FieldElement(7, 13)
    >>> b = FieldElement(6, 13)
    >>> print(a == b)
    False
    >>> print(a == a)
    True

# end::example1[]
# tag::example2[]
    >>> print(7 % 3)
    1

# end::example2[]
# tag::example3[]
    >>> print(-27 % 13)
    12

# end::example3[]
# tag::example4[]
    >>> from ecc import FieldElement
    >>> a = FieldElement(7, 13)
    >>> b = FieldElement(12, 13)
    >>> c = FieldElement(6, 13)
    >>> print(a+b==c)
    True

# end::example4[]
# tag::example5[]
    >>> from ecc import FieldElement
    >>> a = FieldElement(3, 13)
    >>> b = FieldElement(12, 13)
    >>> c = FieldElement(10, 13)
    >>> print(a*b==c)
    True

# end::example5[]
# tag::example6[]
    >>> from ecc import FieldElement
    >>> a = FieldElement(3, 13)
    >>> b = FieldElement(1, 13)
    >>> print(a**3==b)
    True

# end::example6[]
# tag::example7[]
    >>> from ecc import FieldElement
    >>> a = FieldElement(7, 13)
    >>> b = FieldElement(8, 13)
    >>> print(a**-3==b)
    True

# end::example7[]
"""
