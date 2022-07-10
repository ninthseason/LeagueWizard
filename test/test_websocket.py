import asyncio
import logging
import unittest

from core.Network import create_websocket

logging.basicConfig(level=logging.DEBUG)


class MyTestCase(unittest.TestCase):
    def test_something(self):
        async def foo():
            pass

        async def main():
            await create_websocket(foo)

        asyncio.run(main())

if __name__ == '__main__':
    unittest.main()
