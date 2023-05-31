import os
from typing import Optional, Union, Literal, Callable, Coroutine, NoReturn

import aioconsole
import colorama
from colorama import Fore, Style

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


class IndexPage:
    options: dict[str, dict[Literal['text', 'callback'], Union[Callable[[], str], Callable[[], Coroutine]]]] = {}

    banner = (f"*********************************************\n"
              f"** {Style.BRIGHT}League Wizard {Fore.RED}v0.3.0{Fore.RESET}{Style.RESET_ALL}\n"
              f"** Powered by Kl1nge5\n"
              f"*********************************************")

    def __init__(self):
        raise RuntimeError("Class `IndexPage` is a static class. You should not create object from it.")

    @staticmethod
    def add_option(option: dict[Literal['text', 'callback'], Union[Callable[[], str], Callable[[], Coroutine]]]) -> None:
        """
        :param option: The option that need to be added
        :return: None

        Add an option to the index page

        e.m:
        IndexPage.add_option({'text': "启动/关闭自动选择英雄", 'callback': func})
        """
        IndexPage.options.update({str(len(IndexPage.options) + 1): option})

    @staticmethod
    def render(flash_message: str = None) -> None:
        os.system("cls")
        print(IndexPage.banner)
        print(Style.BRIGHT)
        for index in IndexPage.options:
            text_content: str = IndexPage.options[index]['text']()
            text = f"{index}. {text_content}\n"
            print(text)
        print("x. 退出程序")
        print(Style.RESET_ALL)
        if flash_message is not None:
            print(flash_message)
        print("/>", end="")

    @staticmethod
    async def loop() -> NoReturn:
        """
        :return: NoReturn

        Start message loop of IndexPage
        """
        flash_msg: Optional[str] = None
        while True:
            IndexPage.render(flash_msg)
            command: str = await aioconsole.ainput()
            command = command.strip()
            if command == 'x':
                exit()
            elif IndexPage.options.get(command, None) is not None:
                flash_msg = await IndexPage.options[command].get('callback', None)()
            else:
                flash_msg = "未知命令"
