from unittest import TestCase

from ecc import FieldElement, Point, S256Point, ECCTest, G, N
from random import randint
from helper import hash256


class Chapter3Test(TestCase):

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
