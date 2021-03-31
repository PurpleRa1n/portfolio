from http import HTTPStatus
from typing import Dict

from aiohttp.web import json_response

from auth.decorators import login_required
from core import views
from tic_tac_toe.enums import TicTacToeErrors
from tic_tac_toe.models import Game, GameLog
from tic_tac_toe.schemas import GameSchema, GameMoveSchema, GameLogSchema
from tic_tac_toe.services.game import game_service


class GameView(views.BaseView):
    schema_class = GameMoveSchema

    @login_required
    async def post(self):
        """
        Returns a new Game instance.
        """
        game: Game = await game_service.create(self.request.user.id)
        data = GameSchema().dump(game)
        return json_response(data=data, status=HTTPStatus.OK)

    @login_required
    async def patch(self):
        """
        Make a player move. After a successfully player move a computer move will be made. Return a game object with
        made moves.

        Errors:
        - Game already over;
        - Game bounded with other user;
        - Attempt to fill already filled board cell;
        """
        data: Dict = await self.get_validated_data(raise_exception=True)
        game_id: int = int(self.request.match_info['id'])
        game: Game = await self.get_object_or_404(Game, game_id)

        if not game.active:
            return json_response(
                data={'error': TicTacToeErrors.game_already_over.value},
                status=HTTPStatus.BAD_REQUEST
            )

        if game.user_id != self.request.user.id:
            return json_response(
                data={'error': TicTacToeErrors.not_user_game.value},
                status=HTTPStatus.BAD_REQUEST
            )

        game, success = await game_service.process_iteration(game, data)
        if not success:
            return json_response(
                data={'error': TicTacToeErrors.invalid_turn.value},
                status=HTTPStatus.BAD_REQUEST
            )

        data = GameSchema().dump(game)
        return json_response(data=data, status=HTTPStatus.OK)


class GameLogView(views.BaseView):

    @login_required
    async def get(self):
        game_id: int = int(self.request.match_info['id'])
        await self.get_object_or_404(Game, game_id)
        game_logs = await GameLog.query.where(game_id == game_id).gino.all()
        data = GameLogSchema().dump(game_logs, many=True)
        return json_response(data=data, status=HTTPStatus.OK)
