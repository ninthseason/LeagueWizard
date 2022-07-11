from typing import Callable, Coroutine, Any

from .Network import create_websocket


class EventListener:
    listeners: dict[str, Callable[[Any], Coroutine]] = {}

    async def start(self) -> None:
        """
        Start the event listener
        """

        async def exec_event(json_data: list):
            event_name = json_data[2].get("uri", "N/A")
            if event_name in self.listeners:
                await self.listeners[event_name](json_data[2].get("data", "N/A"))

        await create_websocket(exec_event)

    def add_listener(self, listener: dict[str, Callable[[Any], Coroutine]]):
        self.listeners.update(listener)


LeagueEventListener = EventListener()


def register_listener(uri: str):
    """
    :param uri: The uri to listen

    Register a callback for an event
    """

    def decorator(func):
        LeagueEventListener.add_listener({uri: func})

    return decorator
