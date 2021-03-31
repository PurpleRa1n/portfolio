from core.envs.base import *

DATABASES = {
    'DEFAULT': {
        'ENGINE': 'asyncpg',
        'NAME': os.getenv('POSTGRES_DB', ''),
        'USER': os.getenv('POSTGRES_USER', 'portfolio'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'portfolio'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
        'MIN_POOL': os.getenv('POSTGRES_MIN_POOL', 1),
        'MAX_POOL': os.getenv('POSTGRES_MAX_POOL', 10),
        'MIGRATION_ENGINE': 'postgresql',
    }
}
