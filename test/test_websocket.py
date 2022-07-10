import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class MyTestCase(unittest.TestCase):
    def test_something(self):
        pass


if __name__ == '__main__':
    unittest.main()
