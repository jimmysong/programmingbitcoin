from unittest import TestSuite, TextTestRunner


def run_test(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)
