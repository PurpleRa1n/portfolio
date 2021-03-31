from typing import Tuple

from tic_tac_toe import constants
from tic_tac_toe.enums import GameResultEnum
from tic_tac_toe.exceptions import InvalidAIMoveChoice
from tic_tac_toe.models import Game, GameLog
from tic_tac_toe.services.tic_tac_toe import tic_tac_toe_service
from tic_tac_toe.types import Board

_MATCH_RESULT_MAP = {
    constants.DRAW_RESULT: GameResultEnum.draft.value,
    constants.WIN_RESULT: GameResultEnum.player.value,
    constants.LOSE_RESULT: GameResultEnum.computer.value,
}


class GameService:

    @staticmethod
    async def _get_match_result(board: Board) -> int:
        """
        Return external game result.
        """
        internal_result: int = tic_tac_toe_service.get_match_score(board)
        return _MATCH_RESULT_MAP[internal_result]

    @staticmethod
    async def _create_game_log(game: Game) -> GameLog:
        """
        Creates an entity of game log which represent a game step.
        """
        game_log: GameLog = await GameLog.create(game_id=game.id, field=game.field)
        return game_log

    @staticmethod
    def _game_is_active(board: Board) -> bool:
        """
        Return true if:
            - the are no empty cells and now one win
            - someone have a win combination on the board
        Otherwise false
        """
        return not (not tic_tac_toe_service.are_turns_left(board) or tic_tac_toe_service.are_game_over(board))

    async def _make_player_move(self, game: Game, row: int, col: int) -> Tuple[Board, bool]:
        """
        Set player move on the board. Update game object in database and create game log entity.
        Return current board state and game state.
        """
        board = tic_tac_toe_service.set_move(game.field['board'], row, col, constants.PLAYER_VALUE)
        game_is_active: bool = self._game_is_active(board)
        await game.update(active=game_is_active, field={'board': board}).apply()
        await self._create_game_log(game)
        return board, game_is_active

    async def _make_computer_move(self, game: Game, board: Board) -> Game:
        """
        Get coordinates and set computer player move on the board. Update game object in database and
        create game log entity.
        Return current game object.
        """
        row, col = tic_tac_toe_service.get_move_coordinates(board=board)
        if not tic_tac_toe_service.validate_move(game.field['board'], row, col):
            # TBD how to process this case
            raise InvalidAIMoveChoice('Invalid ai move choice.')
        board = tic_tac_toe_service.set_move(board, row, col, constants.COMPUTER_VALUE)
        game_is_active: bool = self._game_is_active(board)
        data = {'active': game_is_active, 'field': {'board': board}}
        if not game_is_active:
            result = self._get_match_result(board)
            data['result'] = result
        await game.update(**data).apply()
        await self._create_game_log(game)
        return game

    async def create(self, user_id: int):
        """
        Return a new game entity.
        """
        board: Board = tic_tac_toe_service.create()
        game: Game = await Game.create(user_id=user_id, field={'board': board})
        await self._create_game_log(game)
        return game

    async def process_iteration(self, game, move_data) -> Tuple[Game, bool]:
        """
        Main method to process a player move. Returns a game instance and current iteration status.
        This method could possibly return a error state in case if current move isn't possible.
        """
        row: int
        col: int
        row, col = move_data['row'], move_data['col']

        if not tic_tac_toe_service.validate_move(game.field['board'], row, col):
            return game, False

        board, is_game_active = await self._make_player_move(game, row, col)
        if not is_game_active:
            return game, True

        game = await self._make_computer_move(game, board)
        return game, True


game_service = GameService()
