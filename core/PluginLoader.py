import importlib
import pathlib


def load_plugins(plugins_folder: str):
    for plugin in pathlib.Path(plugins_folder).iterdir():
        plugin_name: str = plugin.name
        importlib.import_module(f"plugins.{plugin_name}")
