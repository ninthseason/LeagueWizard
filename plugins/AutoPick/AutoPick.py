import logging
from typing import Literal

from httpx import Response

from core.Config import GlobalConfig
from core.Network import create_request


async def choose_champ(action_id: str, action_type: str, champ_id: str) -> Response:
    """
    :param action_id: the `id` field in actor data
    :param action_type: 'pick' or 'ban'
    :param champ_id: id of the champion to choose
    :return: the response data (Always be blank)
    choose a champion by id when select phase
    e.m: choose_champ("1", "pick", "157")
    """
    _options: dict[Literal['url', 'method', 'body'], str | dict] = {
        'url': f"/lol-champ-select/v1/session/actions/{action_id}",
        'method': 'patch',
        'body': {
            "completed": "false",
            "type": action_type,
            "championId": champ_id
        }
    }
    _res = await create_request(_options)
    logging.debug(_res.content)
    return _res


async def auto_choose_champ() -> None:
    """
    Auto select champion
    """
    # get session
    options: dict[Literal['url', 'method', 'body'], str | dict] = {
        "url": "/lol-champ-select/v1/session",
        "method": "get",
    }

    res = (await create_request(options)).json()
    logging.debug(res)
    try:
        local_player_cell_id = res['localPlayerCellId']
        for action in res['actions']:
            for i in action:
                if i['actorCellId'] == local_player_cell_id \
                        and not i['completed'] \
                        and GlobalConfig.get('AutoPick') \
                        and i['type'] == 'pick' \
                        and i['isInProgress']:
                    await choose_champ(str(i['id']), 'pick', str(GlobalConfig.get('AutoPickChampId')))
    except KeyError:
        logging.error('[AutoPick]Can not get game data. Are you in select phase?')
