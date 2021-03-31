from enum import Enum


class AuthErrors(Enum):
    auth_required = 'Authentication token required.'
    invalid_token = 'Token is invalid.'
