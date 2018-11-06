from unittest import SkipTest, TestSuite, TextTestRunner


@SkipTest
def run_test(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)
