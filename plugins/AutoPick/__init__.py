from core.EventListener import register_listener
from .AutoPick import auto_choose_champ


@register_listener("/lol-gameflow/v1/gameflow-phase")
async def change_phase_event(data):
    if data == "ChampSelect":
        await auto_choose_champ()
