from typing import Tuple

from tic_tac_toe.constants import EMPTY_CELL
from tic_tac_toe.types import Board


def get_board_filled_cell(board: Board) -> Tuple[int, int]:
    """
    Check board an return an already filled cell.
    """
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            if board[x][y] != EMPTY_CELL:
                return x, y
    raise AssertionError('The board doen\'t have a filled cell.')
