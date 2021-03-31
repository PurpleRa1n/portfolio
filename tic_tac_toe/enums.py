import enum


class GameResultEnum(enum.Enum):
    pending = 0
    draft = 1
    player = 2
    computer = 3


class TicTacToeErrors(enum.Enum):
    invalid_turn = 'Invalid turn.'
    game_already_over = 'The game is already over.'
    not_user_game = 'This is not your game.'
