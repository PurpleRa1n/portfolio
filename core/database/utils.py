import os
from pathlib import Path
from types import SimpleNamespace
from typing import Dict
from typing import Optional, Union

from alembic.config import Config
from configargparse import Namespace

from core import settings


PROJECT_PATH = Path(__file__).parent.parent.parent.resolve()
_ALEMBIC_DSN_KEY = 'sqlalchemy.url'



def get_gino_database_config(database: str = None) -> Dict:
    """
    Returns the database connection nginx-custom.conf in a gino-friendly format.

    Optionally accepts a database as an argument to be able to flexibly configure connections to
    different databases within one DBMS.
    """
    db_config = settings.DATABASES['DEFAULT']
    config = {
        'driver': db_config['ENGINE'],
        'port': db_config['PORT'],
        'database': db_config['NAME'],
        'host': db_config['HOST'],
        'user': db_config['USER'],
        'password': db_config['PASSWORD'],
        'pool_min_size': db_config['MIN_POOL'],
        'pool_max_size': db_config['MAX_POOL'],
    }
    if database is not None:
        config['database'] = database
    return config


def get_database_dsn(is_migration: bool = False) -> str:
    """
    Returns the database DSN.

    The migration parameter determines which driver will be taken from the settings.
    """

    db_config: Dict = settings.DATABASES['DEFAULT']
    engine: str = db_config["ENGINE"] if not is_migration else db_config['MIGRATION_ENGINE']

    return (
        f'{engine}://{db_config["USER"]}:{db_config["PASSWORD"]}'
        f'@{db_config["HOST"]}:{db_config["PORT"]}/{db_config["NAME"]}'
    )


def get_database_name():
    return settings.DATABASES['DEFAULT']['NAME']


def make_alembic_config(cmd_opts: Union[Namespace, SimpleNamespace], base_path: str = PROJECT_PATH) -> Config:
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)

    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option('script_location', os.path.join(base_path, alembic_location))
    if cmd_opts.db_dsn:
        config.set_main_option(_ALEMBIC_DSN_KEY, cmd_opts.db_dsn)

    return config


def alembic_config_from_url(db_dsn: Optional[str] = None) -> Config:
    """
    Provides Python object, representing alembic.ini file.
    """
    cmd_options = SimpleNamespace(
        config='alembic.ini',
        name='alembic',
        db_dsn=db_dsn,
        raiseerr=False,
        x=None,
    )

    return make_alembic_config(cmd_options)
