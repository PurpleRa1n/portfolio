from http import HTTPStatus

import pytest

from tests.constants import Urls
from tests.tic_tac_toe import constants
from tic_tac_toe.constants import EMPTY_BOARD
from tic_tac_toe.enums import GameResultEnum
from tic_tac_toe.models import Game, GameLog
from tic_tac_toe.schemas import GameSchema
from tic_tac_toe.services.tic_tac_toe import tic_tac_toe_service
from tic_tac_toe.types import Board, PlayerValue


@pytest.fixture
async def game(api_client, token_hdr):
    """
    Returns a game instance created through api.
    """
    response = await api_client.post(Urls.tic_tac_toe.value, headers=token_hdr)
    assert response.status == HTTPStatus.OK
    response_data = await response.json()
    assert True is response_data['active']
    yield response_data


@pytest.fixture
async def game_with_step(api_client, user):
    """
    Returns a game instance with user step.
    """
    game = await Game.create(
        user_id=user['id'],
        field={'board': constants.BOARD_WITH_STEP},
    )
    game_data = GameSchema().dump(game)
    yield game_data


@pytest.fixture
async def finished_game(api_client, user):
    """
    Manually create a game/game logs with manual moves to reduce load time.
    """
    async def process_step(row: int, col: int, game: Game, board: Board, player_move: PlayerValue):
        board = tic_tac_toe_service.set_move(board, row, col, player_move)
        await game.update(field={'board': board}).apply()
        await GameLog.create(game_id=game.id, field=game.field)
        return board

    board = EMPTY_BOARD.copy()
    game = await Game.create(user_id=user['id'], field={'board': board})

    steps = [
        (0, 0, 1),
        (0, 2, -1),
        (0, 1, 1),
        (0, 1, -1),
        (0, 2, 1),
    ]
    for step in steps:
        row, col, player_move = step
        board = await process_step(row, col, game, board, player_move)
    await game.update(active=False, result=GameResultEnum.player.value).apply()
    game_data = GameSchema().dump(game)

    yield game_data
