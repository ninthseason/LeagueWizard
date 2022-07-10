# The file is not a part of main app.
# It is a developer tool
import asyncio
import time

from core.Network import create_websocket


async def start():
    async def exec_event(json_data: list):
        time_text = "[%0.2d:%0.2d:%0.2d]" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        log_text = time_text + str(json_data) + "\n"
        print(log_text)
        with open("EventLog.txt", "a+") as f:
            f.writelines(log_text)

    await create_websocket(exec_event)


asyncio.run(start())
