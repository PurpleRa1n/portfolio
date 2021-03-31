from typing import List

from tic_tac_toe.types import Board


EMPTY_CELL: int = 0
EMPTY_BOARD: Board = [
    [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
    [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
    [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
]
PLAYER_VALUE: int = 1
COMPUTER_VALUE: int = -1

MAX_DEPTH: int = 9
MIN_DEPTH: int = 0

ROWS: List[int] = [0, 1, 2]
COLS: List[int] = ROWS

DRAW_RESULT = 0
WIN_RESULT = 1
LOSE_RESULT = -1
