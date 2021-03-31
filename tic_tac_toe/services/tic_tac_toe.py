import math
import random
from typing import List, Tuple

from tic_tac_toe import constants
from tic_tac_toe.types import Board, PlayerValue


class TicTacToeService:

    @staticmethod
    def _wins(board: Board, player_value: PlayerValue) -> bool:
        """
        Check if a specific player wins
        """
        win_combinations: Board = [
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            [board[0][0], board[1][1], board[2][2]],
            [board[2][0], board[1][1], board[0][2]],
        ]
        return [player_value, player_value, player_value] in win_combinations

    @staticmethod
    def _empty_cells(board: Board) -> List[List[int]]:
        """
        Return list of empty cells
        """
        cells = []

        for idx_r, row in enumerate(board):
            for idx_y, cell in enumerate(row):
                if cell == 0:
                    cells.append([idx_r, idx_y])

        return cells

    def create(self) -> Board:
        """
        Creates a new board.
        It can randomly make the first move of the computer and return the board with the move or return just
        an empty field.
        """
        is_ai_goes_first: bool = bool(random.getrandbits(1))
        if is_ai_goes_first:
            row: int
            col: int
            row, col = self.get_move_coordinates(board=constants.EMPTY_BOARD)
            board = self.set_move(board=constants.EMPTY_BOARD, row=row, col=col, move_value=constants.COMPUTER_VALUE)
            return board
        return constants.EMPTY_BOARD

    def are_game_over(self, board: Board) -> bool:
        """
        Verify if somebody win a party.
        """
        return self._wins(board, constants.PLAYER_VALUE) or self._wins(board, constants.PLAYER_VALUE)

    def get_move_coordinates(
            self,
            board: List[List[int]],
            player_value: int = constants.COMPUTER_VALUE
    ) -> Tuple[int, int]:
        """
        Returns coordinates for the move
        """
        depth = len(self._empty_cells(board))
        if depth == constants.MAX_DEPTH:
            return random.choice(constants.ROWS), random.choice(constants.COLS)
        row: int
        col: int
        row, col, _ = self.calculate_best_move(board, depth, player_value)
        return row, col

    def validate_move(self, board: Board, row: int, col: int):
        """
        Return true if cell is empty otherwise false.
        """
        empty_cells = self._empty_cells(board)
        return [row, col] in empty_cells

    def set_move(self, board: Board, row: int, col: int, move_value: PlayerValue) -> Board:
        """
        Set the move on board.
        """
        board[row][col] = move_value
        return board

    def calculate_best_move(self, board: Board, depth: int, player_value: PlayerValue) -> List[int]:
        """
        Base on minimax algorithm calculates the best possible move for current board state.
        More info could be found here: https://en.wikipedia.org/wiki/Minimax
        """
        best = (
            [-1, -1, -math.inf]
            if player_value == constants.COMPUTER_VALUE
            else [-1, -1, math.inf]
        )

        if depth == 0 or self.are_game_over(board):
            score = self._get_match_score(board)
            return [-1, -1, score]

        for cell in self._empty_cells(board):
            x, y = cell[0], cell[1]
            board[x][y] = player_value
            score = self.calculate_best_move(board, depth - 1, -player_value)
            board[x][y] = 0
            score[0], score[1] = x, y

            if player_value == constants.COMPUTER_VALUE:
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score

        return best

    def _get_match_score(self, board: Board) -> int:
        """
        Function intend to calculate a match result for internal usage of ai algorithm.
        (!) Pay attention that this function consider win result for Computer value.
        """
        score = constants.DRAW_RESULT
        if self._wins(board, constants.COMPUTER_VALUE):
            score = constants.WIN_RESULT
        elif self._wins(board, constants.PLAYER_VALUE):
            score = constants.LOSE_RESULT
        return score

    def get_match_score(self, board: Board) -> int:
        """
        Normal method to identify the winner result.
        """
        score = constants.DRAW_RESULT
        if self._wins(board, constants.PLAYER_VALUE):
            score = constants.WIN_RESULT
        elif self._wins(board, constants.COMPUTER_VALUE):
            score = constants.LOSE_RESULT
        return score

    def are_turns_left(self, board: Board) -> bool:
        """
        Check if there are empty cells left
        """
        return not len(self._empty_cells(board)) == constants.MIN_DEPTH


tic_tac_toe_service = TicTacToeService()
