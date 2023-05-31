import asyncio
from typing import Callable, Coroutine, Any

from .Network import create_websocket


class EventListener:
    listeners: dict[str, list[Callable[[Any], Coroutine]]] = {}

    async def start(self) -> None:
        """
        Start the event listener
        """

        async def exec_event(json_data: list):
            event_name = json_data[2].get("uri", "N/A")
            if event_name in self.listeners:
                for i in self.listeners[event_name]:
                    asyncio.create_task(i(json_data[2].get("data", "N/A")))

        await create_websocket(exec_event)

    def add_listener(self, uri: str, listener: Callable[[Any], Coroutine]):
        if self.listeners.get(uri) is None:
            self.listeners[uri] = []
        self.listeners[uri].append(listener)


LeagueEventListener = EventListener()


def register_listener(uri: str):
    """
    :param uri: The uri to listen

    Register a callback for an event
    """

    def decorator(func):
        LeagueEventListener.add_listener(uri, func)

    return decorator
