import unittest

from Authentication import ClientData
from Network import create_request


class MyTestCase(unittest.TestCase):
    def test_something(self):
        options = {
            "url": "/lol-champ-select/v1/session",
            "method": "get",
            # "body": {
            #
            # }
        }
        print(create_request(options, ClientData))


if __name__ == '__main__':
    unittest.main()
