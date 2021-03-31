from typing import Dict

from core import settings


def get_gino_database_config(database: str = None) -> Dict:
    """
    Returns the database connection config in a gino-friendly format.

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


def get_database_name() -> str:
    return settings.DATABASES['DEFAULT']['NAME']
