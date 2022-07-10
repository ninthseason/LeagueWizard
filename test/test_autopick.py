import asyncio
import unittest

from plugins.AutoPick import auto_choose_champ


class MyTestCase(unittest.TestCase):
    def test_something(self):
        asyncio.run(auto_choose_champ())


if __name__ == '__main__':
    unittest.main()
