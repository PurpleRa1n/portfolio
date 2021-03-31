from http import HTTPStatus

import pytest
from alembic.command import upgrade
from tests.constants import Urls, CREDENTIALS, CREDENTIALS2
from tests.utils import tmp_database
from tests.validators import validate_type
from yarl import URL

from core.app import create_app
from core.database.utils import get_database_dsn, alembic_config_from_url

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
def test_db_template(db_dsn):
    """
    Creates temporary database and applies alembic migrations.

    This database with migrations used as template to fast creation another clean databases to make
    all tests independent.

    Has "session" scope, so is called only once per tests run.
    """
    with tmp_database(db_dsn, _TEMPLATE_DB_NAME) as tmp_url:
        alembic_config = alembic_config_from_url(tmp_url)
        upgrade(alembic_config, _MIGRATIONS_POSITION)
        yield tmp_url


@pytest.fixture
def test_db(db_dsn, test_db_template):
    """
    Creates clean database with migrations from template.
    """
    template_db = URL(test_db_template).name
    with tmp_database(db_dsn, _TEST_DB_SUFFIX, template=template_db) as tmp_url:
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


@pytest.fixture
async def user(api_client):
    """
    Creates a user in database.
    """
    response = await api_client.post(Urls.registration.value, json=CREDENTIALS)
    assert response.status == HTTPStatus.CREATED
    response_data = await response.json()
    yield response_data


@pytest.fixture
async def token_hdr(api_client, user):
    """
    Returns ready to use valid header with auth token.
    """
    response = await api_client.post(Urls.login.value, json=CREDENTIALS)
    assert response.status == HTTPStatus.OK
    response = await response.json()
    assert response['token'] == validate_type(str)
    yield {'authorization': response['token']}


@pytest.fixture
async def user2(api_client):
    """
    Creates a second user in database.
    """
    response = await api_client.post(Urls.registration.value, json=CREDENTIALS2)
    assert response.status == HTTPStatus.CREATED
    response_data = await response.json()
    yield response_data


@pytest.fixture
async def token_hdr2(api_client, user2):
    """
    Returns ready to use valid header with auth token for second user.
    """
    response = await api_client.post(Urls.login.value, json=CREDENTIALS2)
    assert response.status == HTTPStatus.OK
    response = await response.json()
    assert response['token'] == validate_type(str)
    yield {'authorization': response['token']}
