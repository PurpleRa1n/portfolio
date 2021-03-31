import os
import uuid
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, Union

from alembic.config import Config
from configargparse import Namespace
from sqlalchemy_utils import create_database, drop_database
from yarl import URL

PROJECT_PATH = Path(__file__).parent.parent.parent.resolve()
_ALEMBIC_DSN_KEY = 'sqlalchemy.url'


def make_alembic_config(cmd_opts: Union[Namespace, SimpleNamespace], base_path: str = PROJECT_PATH) -> Config:
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)

    if cmd_opts.pg_url:
        config.set_main_option(_ALEMBIC_DSN_KEY, cmd_opts.pg_url)

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


@contextmanager
def tmp_database(db_url: URL, suffix: str = '', **kwargs):
    """
    Creates a temporary database that is automatically deleted after tests;
    """
    tmp_db_name = '.'.join([uuid.uuid4().hex, suffix])
    tmp_db_url = str(db_url.with_path(tmp_db_name))

    create_database(tmp_db_url, **kwargs)

    try:
        yield tmp_db_url
    finally:
        drop_database(tmp_db_url)
