import aioconsole

from core.IndexPage import IndexPage
from .ApplyPerk import RuneSystem

RuneSystem.read_data_from_file()


async def save_current_rune_callback():
    res = await RuneSystem.save_current_rune()
    if res:
        return "保存成功"
    else:
        return "操作取消"


async def apply_rune_callback():
    res = await RuneSystem.render()
    if res is None:
        return "无可用符文"
    target_id: str = await aioconsole.ainput("请输入目标符文id:\n/>")
    if target_id.strip() == "":
        return "操作取消"
    try:
        await RuneSystem.apply_rune(res[target_id])
        return f"成功应用符文: {res[target_id]}"
    except KeyError:
        return "无效id"


async def manage_rune_callback():
    res = await RuneSystem.render()
    if res is None:
        return "无可用符文"
    target_id: str = await aioconsole.ainput("请输入目标符文id:\n/>")
    if target_id.strip() == "":
        return "操作取消"
    try:
        await RuneSystem.del_local_page(res[target_id])
        return f"成功删除符文: {res[target_id]}"
    except KeyError:
        return "无效id"


IndexPage.add_option({'text': lambda: "保存当前符文", 'callback': save_current_rune_callback})
IndexPage.add_option({'text': lambda: "应用符文", 'callback': apply_rune_callback})
IndexPage.add_option({'text': lambda: "删除符文", 'callback': manage_rune_callback})
