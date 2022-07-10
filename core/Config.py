import json
import logging
import pathlib
from typing import Any


class GlobalConfig:
    __configs: dict[str, Any] = {}
    config_file_path: str = None

    @staticmethod
    def get(item: str):
        return GlobalConfig.__configs.get(item, None)

    @staticmethod
    def update(new_entry: dict):
        GlobalConfig.__configs.update(new_entry)
        GlobalConfig.save_to_file()

    @staticmethod
    def save_to_file():
        assert GlobalConfig.config_file_path is not None, "配置文件路径未设置"
        with open(GlobalConfig.config_file_path, "w") as f:
            json.dump(GlobalConfig.__configs, f)

    @staticmethod
    def read_from_file():
        assert GlobalConfig.config_file_path is not None, "配置文件路径未设置"
        try:
            with open(GlobalConfig.config_file_path, "r") as f:
                GlobalConfig.__configs = json.load(f)
        except FileNotFoundError:
            logging.warning("未找到配置文件，将自动生成。")

    @staticmethod
    def check(item: str) -> bool:
        """
        :param item: The config name to check
        :return: bool

        Check a config entry whether have been recorded
        """
        return True if (GlobalConfig.__configs.get(item, None) is not None) else False

    @staticmethod
    def set_config_file_path(path: str):
        if pathlib.Path(path).is_dir():
            raise RuntimeError("配置文件路径无效")
        GlobalConfig.config_file_path = path
        GlobalConfig.read_from_file()
