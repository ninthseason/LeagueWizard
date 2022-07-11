import aioconsole
from colorama import Fore

from core.Config import GlobalConfig
from core.EventListener import register_listener
from core.IndexPage import IndexPage
from .AutoPick import auto_choose_champ

if not GlobalConfig.check('AutoPick'):
    GlobalConfig.update({'AutoPick': True})
if not GlobalConfig.check('AutoPickChampId'):
    GlobalConfig.update({'AutoPickChampId': 157})


@register_listener("/lol-gameflow/v1/gameflow-phase")
async def change_phase_event(data):
    if data == "ChampSelect":
        await auto_choose_champ()


async def switch_auto_pick():
    GlobalConfig.update({'AutoPick': not GlobalConfig.get('AutoPick')})


def auto_pick_text():
    return f"{Fore.GREEN if GlobalConfig.get('AutoPick') else Fore.RED}开启/关闭自动选择英雄{Fore.RESET}"


async def change_auto_pick_champ():
    new_id: str = await aioconsole.ainput("请输入目标英雄id:\n/>")
    if new_id.strip() == "":
        return "操作取消"
    try:
        new_id: int = int(new_id)
    except ValueError:
        return "id格式错误"
    GlobalConfig.update({'AutoPickChampId': new_id})


def change_id_text():
    return f"更改英雄选择 {Fore.CYAN}<{GlobalConfig.get('AutoPickChampId')}>{Fore.RESET}"


IndexPage.add_option({"text": auto_pick_text, "callback": switch_auto_pick})
IndexPage.add_option({"text": change_id_text, "callback": change_auto_pick_champ})
