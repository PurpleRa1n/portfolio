import os

from core.enums import EnvironmentEnum
from core.exceptions import ImproperlyConfigured

APP_ENVIRONMENT = os.getenv('APP_ENVIRONMENT', EnvironmentEnum.dev.value)

if APP_ENVIRONMENT == EnvironmentEnum.dev.value:
    from core.envs.base import *
elif APP_ENVIRONMENT == EnvironmentEnum.test.value:
    from core.envs.test import *
else:
    raise ImproperlyConfigured(f'Application settings for the environment of the {APP_ENVIRONMENT} are missing.')
