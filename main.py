import asyncio
import os
from typing import Union, Optional

import aioconsole
import colorama
from colorama import Fore, Style

from Config import global_configs
from EventListener import LeagueEventListener

colorama.init()


def config_format(config: Union[bool, str, int]) -> str:
    """
    :param config: the config need to be formatted
    :return: string after formatted

    turn a config value to a printtable format
    """
    if isinstance(config, bool):
        return Fore.GREEN if config else Fore.RED
    elif isinstance(config, str):
        return config
    elif isinstance(config, int):
        return str(config)


def render(flash_message: Optional[str]) -> None:
    """
    :param flash_message: the extra message that need to be printed

    Render the main index.
    """
    os.system("cls")
    banner = f"""*********************************************
** {Style.BRIGHT}League Wizard {Fore.RED}v0.1.0{Fore.RESET}{Style.RESET_ALL}
** Powered by Kl1nge5
*********************************************"""
    print(banner)

    features = f"""{Style.BRIGHT}
1. {config_format(global_configs.get('AutoPick'))}启动/关闭自动选择英雄{Fore.RESET}

2. 更换英雄 <{Fore.CYAN}{config_format(global_configs.get('AutoPickChampId'))}{Fore.RESET}>

3. 退出程序
{Style.RESET_ALL}"""
    print(features)
    if flash_message is not None:
        print(flash_message)


async def cli():
    flash_msg = None
    while True:
        render(flash_msg)
        command: str = await aioconsole.ainput("/>")
        command = command.strip()
        if command == "1":
            global_configs.update({"AutoPick": not global_configs.get("AutoPick")})
            flash_msg = None
        elif command == "2":
            new_id = await aioconsole.ainput("请输入新的英雄id:\n")
            try:
                new_id = int(new_id)
                if not (0 <= new_id <= 300):
                    raise ValueError
                global_configs.update({"AutoPickChampId": new_id})
                flash_msg = None
            except ValueError:
                flash_msg = "无效ID"
        elif command == "3":
            exit()
        else:
            flash_msg = "未知命令"


async def main():
    cli_task = asyncio.create_task(cli())
    event_listener_task = asyncio.create_task(LeagueEventListener.start())

    await cli_task


asyncio.run(main())
