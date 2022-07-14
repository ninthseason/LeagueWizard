import aioconsole
from colorama import Fore

from core.Config import GlobalConfig
from core.EventListener import register_listener
from core.IndexPage import IndexPage
from .AutoPick import auto_choose_champ

# 检查全局配置是否拥有指定条目，若没有则用默认值创建
# GlobalConfig.check('') 用于检查全局配置是否存在条目
# GlobalConfig.update({}) 用于更新全局配置
if not GlobalConfig.check('AutoPick'):
    GlobalConfig.update({'AutoPick': True})
if not GlobalConfig.check('AutoPickChampId'):
    GlobalConfig.update({'AutoPickChampId': 157})


# 通过装饰器为事件注册回调函数
#
# @register_listener("<事件uri>")
# def callback_func():
#    ...
#
# 事件uri可以通过 https://github.com/HextechDocs/lcu-explorer 查询
@register_listener("/lol-gameflow/v1/gameflow-phase")
async def change_phase_event(data):
    if data == "ChampSelect":
        await auto_choose_champ()


# 主菜单选项1回调函数
async def switch_auto_pick():
    GlobalConfig.update({'AutoPick': not GlobalConfig.get('AutoPick')})


# 主菜单选项1显示文本
def auto_pick_text():
    return f"{Fore.GREEN if GlobalConfig.get('AutoPick') else Fore.RED}开启/关闭自动选择英雄{Fore.RESET}"


# 主菜单选项2回调函数
async def change_auto_pick_champ():
    new_id: str = await aioconsole.ainput("请输入目标英雄id:\n/>")
    if new_id.strip() == "":
        return "操作取消"
    try:
        new_id: int = int(new_id)
    except ValueError:
        return "id格式错误"
    GlobalConfig.update({'AutoPickChampId': new_id})


# 主菜单选项2显示文本
def change_id_text():
    return f"更改英雄选择 {Fore.CYAN}<{GlobalConfig.get('AutoPickChampId')}>{Fore.RESET}"


# 为主菜单添加两个选项
# IndexPage.add_option({'text': 文本函数, 'callback': 异步回调函数})
# 文本函数返回显示的文本，在每次渲染主菜单时调用
# 异步回调函数在该选项被选择时调用，并立即await
IndexPage.add_option({"text": auto_pick_text, "callback": switch_auto_pick})
IndexPage.add_option({"text": change_id_text, "callback": change_auto_pick_champ})
