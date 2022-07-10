import json
import logging
import os
from typing import Any

base_dir = os.path.dirname(__file__)


class Config:
    name: str = ""
    configs: dict[str, Any] = {}

    def __init__(self, name):
        self.name = name
        self.read_from_file()

    def __getitem__(self, item):
        return self.configs[item]

    def get(self, item):
        return self[item]

    def update(self, new_entry: dict):
        self.configs.update(new_entry)
        self.save_to_file()

    def save_to_file(self):
        with open(base_dir + "/" + self.name + "_config.json", "w") as f:
            json.dump(self.configs, f)

    def read_from_file(self):
        try:
            with open(base_dir + "/" + self.name + "_config.json", "r") as f:
                self.configs = json.load(f)
        except FileNotFoundError:
            logging.warning("未找到配置文件，将自动生成。")
            global_configs.update({'AutoPick': True})
            global_configs.update({'AutoPickChampId': 157})

    def __str__(self):
        return str(self.configs)


global_configs = Config('global')
