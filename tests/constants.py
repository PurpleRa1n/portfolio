from enum import Enum

USERNAME_TEST = 'foobar'
USERNAME_TEST2 = 'foobarQ'
PASSWORD_TEST = 'tryhackme'

CREDENTIALS = {
    'username': USERNAME_TEST,
    'password': PASSWORD_TEST,
}

CREDENTIALS2 = {
    'username': USERNAME_TEST2,
    'password': PASSWORD_TEST,
}


class Urls(Enum):
    login = '/api/v1/auth/login/'
    registration = '/api/v1/auth/registration/'
    health_check = '/health-check/'
    tic_tac_toe = '/api/v1/tic-tac-toe/'
