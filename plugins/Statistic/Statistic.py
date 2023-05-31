import pathlib
import time
import datetime
from typing import Literal, Optional, IO
import json

from core.Network import simple_request
from core.Timer import Timer
from core.IndexPage import IndexPage

data_path = pathlib.Path(__file__).with_name("data")
if not data_path.exists():
    data_path.mkdir()
writer: Optional[IO] = None

_is_recording: bool = False


def is_recording() -> bool:
    return _is_recording


def filename_by_time():
    return data_path.joinpath(datetime.datetime.now().strftime("%Y-%m-%d %H-%M") + ".json")


async def get_game_data(timer_name, context, timer):
    _res = await simple_request("/liveclientdata/activeplayer")
    if _res.status_code == 200:
        if context["first"]:
            context["first"] = False
        else:
            writer.write(f',')
        writer.write(f'"{time.time()}":')
        writer.write(json.dumps(_res.json()["championStats"]))


statistic_timer: Optional[Timer] = None


def start_statistic():
    global writer, _is_recording, statistic_timer
    _is_recording = True
    writer = open(data_path.joinpath(filename_by_time()), "w")
    writer.write("{")
    statistic_timer = Timer(interval=5, first_immediately=False, timer_name="Statistic Timer",
                            context={"first": True}, callback=get_game_data)
    IndexPage.render()


def stop_statistic():
    global statistic_timer, _is_recording
    _is_recording = False
    if writer is not None:
        writer.write("}")
        writer.close()
    if statistic_timer is not None:
        statistic_timer.cancel()
    IndexPage.render()