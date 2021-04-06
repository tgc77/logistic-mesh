import unittest
from . import test_app


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(test_app))

    return suite


if __name__ == '__main__':
    unittest.main(verbosity=2)
