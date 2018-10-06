from unittest import TestSuite, TextTestRunner

import hashlib


def run_test(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)


def double_sha256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()
