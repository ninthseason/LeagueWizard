import importlib
import pathlib


def load_plugins(plugins_folder: str) -> None:
    """
    :param plugins_folder: the path of plugin folder
    :return: None

    load all plugins in the input folder
    """
    for plugin in pathlib.Path(plugins_folder).iterdir():
        plugin_name: str = plugin.name
        importlib.import_module(f"plugins.{plugin_name}")
