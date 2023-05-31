import base64
import json
import logging
import pathlib
import ssl
from typing import Coroutine, Callable, Literal, Union

import httpx
import websockets
from httpx import Response

from .Authentication import ClientData


async def create_request(options: dict[Literal['url', 'method', 'body'], Union[str, dict]],
                         credentials: ClientData = ClientData) -> Response:
    """
    :param options: dict[str, Any]
    :param credentials: ClientData from Authentication.py
    :return: The response dat

    Make an HTTPS request to Client.
    options' struct as:
    {
        "url": str       # the url to request e.m: "/lol-champ-select/v1/session"
        "method: str     # the request method e.m: "get"
        "body"?: dict    # the request body
    }
    """
    host: str = '127.0.0.1'
    port: int = credentials.port
    url: str = options['url']
    path: str = "https://" + host + ":" + str(port) + url
    # logging.debug(path)
    method: str = options['method']
    body: dict = options.get("body", None)

    headers: dict = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64.b64encode(("riot:" + credentials.password).encode()).decode(),
    }

    # Do not need the agent temporarily
    agent: str = ""

    # verify=False temporarily
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.request(method, path, headers=headers, json=body)
    # logging.debug(response.request.content)
    return response


async def create_websocket(func: Callable[[list], Coroutine], credentials: ClientData = ClientData) -> None:
    """
    :param func: The callback function after receive data from client. Receive a parameter: ws_data
    :param credentials: Default
    :return: None

    Create a websocket connection to client.
    """
    path: str = f"wss://riot:{credentials.password}@127.0.0.1:{ClientData.port}/"
    logging.debug(path)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    localhost_pem = pathlib.Path(__file__).with_name("riotgames.pem")
    try:
        ssl_context.load_verify_locations(localhost_pem)
    except FileNotFoundError:
        raise FileNotFoundError("缺少ssl证书文件")
    while True:
        async with websockets.connect(path, ssl=ssl_context) as websocket:
            logging.info("[Network]WebSocket连接成功")
            try:
                await websocket.send(json.dumps([5, 'OnJsonApiEvent']))
                while True:
                    msg = await websocket.recv()
                    try:
                        json_data: list = json.loads(msg)
                        await func(json_data)
                    except json.decoder.JSONDecodeError:
                        pass
            except websockets.ConnectionClosed:
                pass
            except ConnectionRefusedError:
                logging.warning("检测到游戏关闭，助手进入离线状态")
                # exit()


async def simple_request(url: str) -> Response:
    """
    :param url: str
    :return: The response dat

    Make a Simple(without credentials) HTTPS request to Client.
    Always used to call Live Client Data API.
    https://developer.riotgames.com/docs/lol#league-client-api
    """
    path: str = "https://127.0.0.1:2999" + url
    # logging.debug(path)
    method: str = "get"

    # Do not need the agent temporarily
    agent: str = ""

    # verify=False temporarily
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.request(method, path)
    # logging.debug(response.request.content)
    return response
