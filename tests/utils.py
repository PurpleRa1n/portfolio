import uuid
from contextlib import contextmanager

from sqlalchemy_utils import create_database, drop_database
from yarl import URL


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
