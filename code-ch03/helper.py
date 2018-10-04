from unittest import TestCase, TestSuite, TextTestRunner


def run_test(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)
