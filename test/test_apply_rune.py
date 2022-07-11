import asyncio
import logging
import unittest

from plugins.ApplyPerk.ApplyPerk import RuneSystem

logging.basicConfig(level=logging.DEBUG)


class MyTestCase(unittest.TestCase):
    def test_something(self):
        async def main():
            rune_page = await RuneSystem.get_current_rune()
            print(rune_page)

        asyncio.run(main())


if __name__ == '__main__':
    unittest.main()
