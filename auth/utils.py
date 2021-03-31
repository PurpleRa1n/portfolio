import datetime

import jwt

from core import settings
from core.utils import timezone


def get_token_expiration_date() -> datetime:
    return timezone.now() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS)


def get_jwt_token(user_id: int) -> bytes:
    data = {
        'user_id': user_id,
        'exp': get_token_expiration_date(),
    }
    return jwt.encode(data, settings.JWT_SECRET, settings.JWT_ALGORITHM)
