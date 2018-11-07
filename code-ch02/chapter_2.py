from unittest import TestCase

from ecc import Point


class Chapter2Test(TestCase):

    def test_apply(self):

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
            if self == other:
                if self.y == 0 * self.x:
                    return self.__class__(None, None, self.a, self.b)
                else:
                    s = (3 * self.x**2 + self.a) / (2 * self.y)
                    x = s**2 - 2 * self.x
                    y = s * (self.x - x) - self.y
                    return self.__class__(x, y, self.a, self.b)

        Point.__ne__ = ne
        Point.__add__ = add

    def test_example_1(self):
        p1 = Point(-1, -1, 5, 7)
        with self.assertRaises(ValueError):
            p2 = Point(-1, -2, 5, 7)

    def test_exercise_1(self):

        def on_curve(x, y):
            return y**2 == x**3 + 5*x + 7

        self.assertEqual(on_curve(2,4), False)
        self.assertEqual(on_curve(-1,-1), True)
        self.assertEqual(on_curve(18,77), True)
        self.assertEqual(on_curve(5,7), False)

    def test_example_2(self):
        p1 = Point(-1, -1, 5, 7)
        p2 = Point(-1, 1, 5, 7)
        inf = Point(None, None, 5, 7)
        self.assertEqual(p1 + inf, p1)
        self.assertEqual(inf + p2, p2)
        self.assertEqual(p1 + p2, inf)
        
    def test_exercise_3(self):
        def on_curve(x, y):
            return y**2 == x**3 + 5*x + 7
        self.assertEqual(on_curve(2,4), False)
        self.assertEqual(on_curve(-1,-1), True)
        self.assertEqual(on_curve(18,77), True)
        self.assertEqual(on_curve(5,7), False)

    def test_exercise_4(self):
        x1, y1 = 2, 5
        x2, y2 = -1, -1
        s = (y2 - y1) / (x2 - x1)
        x3 = s**2 - x1 - x2
        y3 = s * (x1 - x3) - y1
        self.assertEqual((x3, y3), (3.0, -7.0))

    def test_exercise_6(self):
        a, x1, y1 = 5, -1, 1
        s = (3 * x1**2 + a) / (2 * y1)
        x3 = s**2 - 2 * x1
        y3 = s * (x1 - x3) - y1
        self.assertEqual((x3, y3), (18.0, -77.0))
