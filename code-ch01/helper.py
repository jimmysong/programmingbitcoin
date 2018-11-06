from unittest import TestSuite, TextTestRunner


def run(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)
