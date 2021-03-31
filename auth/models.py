from passlib.hash import pbkdf2_sha256

from core.database.orm import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    username = db.Column(
        db.Unicode(30),
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.Unicode(256),
        nullable=False
    )

    def verify_password(self, raw_password):
        return pbkdf2_sha256.verify(raw_password, self.password)

    @staticmethod
    def hash_password(raw_password):
        return pbkdf2_sha256.hash(raw_password)
