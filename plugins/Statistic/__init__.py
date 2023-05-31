from colorama import Fore

from core.Config import GlobalConfig
from core.EventListener import register_listener
from core.IndexPage import IndexPage

from .Statistic import start_statistic, stop_statistic, is_recording
from .Visualization import choose_file_render

# 检查全局配置是否拥有指定条目，若没有则用默认值创建
# GlobalConfig.check('') 用于检查全局配置是否存在条目
# GlobalConfig.update({}) 用于更新全局配置
if not GlobalConfig.check('StatisticEnabled'):
    GlobalConfig.update({'StatisticEnabled': False})


@register_listener("/lol-gameflow/v1/gameflow-phase")
async def change_phase_event(data):
    if GlobalConfig.get('StatisticEnabled'):
        if data == "InProgress":
            start_statistic()
        elif data == "WaitingForStats":
            stop_statistic()


# 主菜单选项1回调函数
async def switch_statistic():
    GlobalConfig.update({'StatisticEnabled': not GlobalConfig.get('StatisticEnabled')})


# 主菜单选项1显示文本
def statistic_text():
    return f"{Fore.GREEN if GlobalConfig.get('StatisticEnabled') else Fore.RED}开启/关闭数据统计" \
           f"{Fore.RESET}{'(记录中)' if is_recording() else ''}"


# 主菜单选项2回调函数
async def generate_statistic():
    return await choose_file_render()


# 主菜单选项2显示文本
def generate_statistic_text():
    return f"生成统计文件"


# 为主菜单添加两个选项
# IndexPage.add_option({'text': 文本函数, 'callback': 异步回调函数})
# 文本函数返回显示的文本，在每次渲染主菜单时调用
# 异步回调函数在该选项被选择时调用，并立即await
IndexPage.add_option({"text": statistic_text, "callback": switch_statistic})
IndexPage.add_option({"text": generate_statistic_text, "callback": generate_statistic})
