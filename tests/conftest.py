import pytest
from alembic.command import upgrade
from yarl import URL

from core.app import create_app
from core.database.utils import get_database_dsn
from tests.utils import tmp_database, alembic_config_from_url

_TEMPLATE_DB_NAME: str = 'template'
_MIGRATIONS_POSITION: str = 'head'
_TEST_DB_SUFFIX = 'pytest'


@pytest.fixture(scope='session')
def db_dsn():
    """
    Provides database DSN for creating temporary databases.
    """
    dsn = get_database_dsn(is_migration=True)
    url = URL(dsn)
    return url


@pytest.fixture(scope='session')
def test_db_template(pg_url):
    """
    Creates temporary database and applies alembic migrations.

    This database with migrations used as template to fast creation another clean databases to make
    all tests independent.

    Has "session" scope, so is called only once per tests run.
    """
    with tmp_database(pg_url, _TEMPLATE_DB_NAME) as tmp_url:
        alembic_config = alembic_config_from_url(tmp_url)
        upgrade(alembic_config, _MIGRATIONS_POSITION)
        yield tmp_url


@pytest.fixture
def test_db(pg_url, migrated_postgres_template):
    """
    Creates clean database with migrations from template.
    """
    template_db = URL(migrated_postgres_template).name
    with tmp_database(pg_url, _TEST_DB_SUFFIX, template=template_db) as tmp_url:
        yield tmp_url


@pytest.fixture
async def api_client(test_db, aiohttp_client):
    """
    Creates aiohttp application and client for it.
    """
    app = create_app(test_db)
    client = await aiohttp_client(app)
    try:
        yield client
    finally:
        await client.close()
