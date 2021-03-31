from enum import Enum


USERNAME_TEST = 'foobar'
PASSWORD_TEST = 'tryhackme'

CREDENTIALS = {
    'username': USERNAME_TEST,
    'password': PASSWORD_TEST,
}

class Urls(Enum):
    login = '/api/v1/auth/login/'
    registration = '/api/v1/auth/registration/'
    health_check = '/health-check/'
