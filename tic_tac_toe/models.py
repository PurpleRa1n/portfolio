from core.database.orm import db
from core.utils import timezone
from tic_tac_toe.enums import GameResultEnum


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(
        db.Integer(),
        primary_key=True,
    )
    field = db.Column(
        db.JSON(),
        default=dict,
        nullable=False
    )
    active = db.Column(
        db.Boolean(),
        default=True,
        nullable=False
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=timezone.now,
        nullable=False
    )
    finished_at = db.Column(
        db.DateTime(timezone=True),
    )
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey('users.id'),
        nullable=False
    )
    result = db.Column(
        db.Integer(),
        default=GameResultEnum.pending.value,
        nullable=False
    )


class GameLog(db.Model):
    __tablename__ = 'game_logs'

    id = db.Column(
        db.Integer(),
        primary_key=True,
    )
    game_id = db.Column(
        db.Integer(),
        db.ForeignKey('games.id'),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=timezone.now,
        nullable=False
    )
    field = db.Column(
        db.JSON(),
        nullable=False
    )
