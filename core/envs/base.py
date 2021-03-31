import os

JWT_EXP_DELTA_SECONDS = 3600
JWT_ALGORITHM = 'HS256'
JWT_SECRET = os.getenv('JWT_SECRET', 'secret')
AUTH_HEADER = 'Authorization'
AUTH_TOKEN_PREFIX = 'Bearer '


MIDDLEWARES = [
    'auth.middlewares.auth_middleware',
]

APP_HOST = "0.0.0.0"
APP_PORT = 8000

DATABASES = {
    'DEFAULT': {
        'ENGINE': 'asyncpg',
        'NAME': os.getenv('POSTGRES_DB', 'portfolio'),
        'USER': os.getenv('POSTGRES_USER', 'portfolio'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'portfolio'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
        'MIN_POOL': os.getenv('POSTGRES_MIN_POOL', 1),
        'MAX_POOL': os.getenv('POSTGRES_MAX_POOL', 10),
        'MIGRATION_ENGINE': 'postgresql',
    }
}
