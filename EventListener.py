from typing import Callable, Coroutine, Any

import AutoPick
from Network import create_websocket


class EventListener:
    listeners: dict[str, Callable[[Any], Coroutine]] = {}

    async def start(self):
        """
        Start the event listener
        """

        async def exec_event(json_data):
            event_name = json_data[2].get("uri", "N/A")
            if event_name in self.listeners:
                await self.listeners[event_name](json_data[2].get("data", "N/A"))

        await create_websocket(exec_event)

    def add_listener(self, listener: dict[str, Callable[[Any], Coroutine]]):
        self.listeners.update(listener)


LeagueEventListener = EventListener()


# Auto pick champion
async def change_phase_event(data):
    if data == "ChampSelect":
        await AutoPick.auto_choose_champ()


LeagueEventListener.add_listener({"/lol-gameflow/v1/gameflow-phase": change_phase_event})
