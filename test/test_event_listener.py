import asyncio
import unittest

from core.EventListener import LeagueEventListener


class MyTestCase(unittest.TestCase):
    def test_something(self):
        async def main():
            task1 = asyncio.create_task(LeagueEventListener.init())

            # await LeagueEventListener.add_listener()

        asyncio.run(main())


if __name__ == '__main__':
    unittest.main()
