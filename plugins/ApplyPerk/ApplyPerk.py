import json
import logging
import os
import pathlib
import time
from typing import Optional, Union, Literal

import aioconsole
from colorama import Fore, Back

from core.Network import create_request
from .RuneMapping import rune_mapping_r

database_file = pathlib.Path(__file__).with_name("data.json")


class RuneSystem:
    __database: dict[str, dict[Literal['name', 'primaryStyleId', 'selectedPerkIds', 'subStyleId'], Union[int, list, str]]] = {}

    """online method"""

    @staticmethod
    async def get_current_rune() -> Optional[dict]:
        res = await create_request({
            'url': '/lol-perks/v1/pages',
            'method': 'get',
        })
        for rune_page in res.json():
            if rune_page['current'] and rune_page['isDeletable'] and rune_page['isValid']:
                return rune_page
        return None

    @staticmethod
    async def del_rune_page(page_id: int = None) -> None:
        if page_id is None:
            logging.warning("符文页删除失败，请切换至可修改的符文页")
        await create_request({
            'url': f"/lol-perks/v1/pages/{page_id}",
            'method': 'delete'
        })

    @staticmethod
    async def add_rune_page(name: str, primary_style_id: int, selected_perk_ids: list[int], sub_style_id: int) -> None:
        await create_request({
            'url': f'/lol-perks/v1/pages',
            'method': 'post',
            'body': {'autoModifiedSelections': [],
                     'current': True,
                     'id': 692646929,
                     'isActive': True,
                     'isDeletable': True,
                     'isEditable': True,
                     'isValid': True,
                     'lastModified': time.time_ns() // 1000000,
                     'name': name,
                     'order': 0,
                     'primaryStyleId': primary_style_id,
                     'selectedPerkIds': selected_perk_ids,
                     'subStyleId': sub_style_id
                     }
        })

    @staticmethod
    async def apply_rune(name: str) -> None:
        assert RuneSystem.__database.get(name, None) is not None, "符文系统出现内部错误"
        page_name: str = RuneSystem.__database[name]['name']
        primary_style_id: int = RuneSystem.__database[name]['primaryStyleId']
        selected_perk_ids: list[int] = RuneSystem.__database[name]['selectedPerkIds']
        sub_style_id: int = RuneSystem.__database[name]['subStyleId']
        current_rune = await RuneSystem.get_current_rune()
        await RuneSystem.del_rune_page(current_rune['id'])
        await RuneSystem.add_rune_page(page_name, primary_style_id, selected_perk_ids, sub_style_id)

    """local method"""

    @staticmethod
    async def save_current_rune() -> None:
        page = await RuneSystem.get_current_rune()
        name = await aioconsole.ainput("请输入保存名称(重名覆盖):\n")
        RuneSystem.__database.update({name: {'name': page['name'],
                                             'primaryStyleId': page['primaryStyleId'],
                                             'selectedPerkIds': page['selectedPerkIds'],
                                             'subStyleId': page['subStyleId']}})
        RuneSystem.save_data_to_file()

    @staticmethod
    async def del_local_page(name: str):
        try:
            RuneSystem.__database.pop(name)
        except KeyError:
            pass

    @staticmethod
    async def render() -> Optional[dict[str, str]]:
        if len(RuneSystem.__database) == 0:
            return None
        os.system('cls')
        serial_mapping: dict[str, str] = {}
        serial: int = 1
        for index in RuneSystem.__database:
            def get_style_color(style_id: int) -> str:
                if style_id == 8000:
                    return Fore.YELLOW
                elif style_id == 8100:
                    return Fore.RED
                elif style_id == 8200:
                    return Fore.BLUE
                elif style_id == 8300:
                    return Fore.CYAN
                elif style_id == 8400:
                    return Fore.GREEN
                else:
                    return ""

            primary_style = RuneSystem.__database[index]["primaryStyleId"]
            sub_style = RuneSystem.__database[index]["subStyleId"]
            rune_text: str = ""
            for idx, rune_id in enumerate(RuneSystem.__database[index]["selectedPerkIds"]):
                if 0 <= idx <= 3:
                    rune_text += (get_style_color(primary_style) + rune_mapping_r[rune_id] + Fore.RESET) + " "
                elif 3 < idx <= 5:
                    rune_text += (get_style_color(sub_style) + rune_mapping_r[rune_id] + Fore.RESET) + " "
                else:
                    rune_text += (rune_mapping_r[rune_id]) + " "

            text = f'{Fore.BLACK}{Back.WHITE}[{serial}] {index}{Fore.RESET}{Back.RESET}: {rune_text}'
            print(text)
            serial_mapping.update({str(serial): index})
            serial += 1
        print('')
        return serial_mapping

    @staticmethod
    def save_data_to_file() -> None:
        with open(database_file, "w") as f:
            json.dump(RuneSystem.__database, f)

    @staticmethod
    def read_data_from_file() -> None:
        try:
            with open(database_file, "r") as f:
                RuneSystem.__database = json.load(f)
        except FileNotFoundError:
            pass
