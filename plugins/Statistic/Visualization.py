import shutil
import aioconsole
import pathlib
import json
import os
from tensorboardX import SummaryWriter
from .translation import championStats

data_path = pathlib.Path(__file__).with_name("tensorboard_data")
if not data_path.exists():
    data_path.mkdir()


def generate_tensorboard_file(filepath: pathlib.Path):
    _filepath = data_path.joinpath(filepath.name[:-5])
    if _filepath.exists():
        shutil.rmtree(_filepath)
    writer = SummaryWriter(logdir=str(_filepath))
    with open(data_path.with_name("data").joinpath(filepath.name), "r") as f:
        data: dict = json.load(f)
        for timestep, i in enumerate(data):
            for j in data[i]:
                if j == "resourceType":
                    continue
                print(timestep)
                writer.add_scalar(f"statistic/{championStats[j]}", data[i][j], timestep, walltime=float(i))

    writer.close()


async def choose_file_render():
    os.system('cls')
    files_list = []
    print("请输入文件序号: \n")
    for i, v in enumerate(pathlib.Path(pathlib.Path(__file__).with_name("data")).iterdir()):
        files_list.append(v)
        print(f"{i}. {v}\n")
    while True:
        idx = (await aioconsole.ainput("/>")).strip()
        if idx == "":
            return
        try:
            idx = int(idx)
            break
        except ValueError:
            pass

    generate_tensorboard_file(files_list[idx])
    return "生成成功！"
