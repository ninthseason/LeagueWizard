import unittest

from core.Authentication import ClientData


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(ClientData.to_string())


if __name__ == '__main__':
    unittest.main()
