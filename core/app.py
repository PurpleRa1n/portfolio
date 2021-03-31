import asyncio
import pathlib
from typing import Dict

import uvloop
from aiohttp import web
from aiohttp.web_app import Application
from yarl import URL

from core.database.orm import db
from core.database.utils import get_gino_database_config

PROJ_ROOT = pathlib.Path(__file__).parent.parent

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def _init_db(app: Application, database_url: str) -> Application:
    """
    Initialize gino orm.
    """
    app['pg'] = db
    db_url = URL(database_url)
    db_config: Dict = get_gino_database_config(db_url.name)
    app['pg'].init_app(app=app, config=db_config)
    return app


def _get_application() -> Application:
    """
    Returns web application instance.
    """
    app: Application = web.Application()
    return app


def create_app(database_dsn: str) -> Application:
    """
    The main entry point for creating a web application and configuring it.
    """
    app: Application = _get_application()
    app = _init_db(app, database_url=database_dsn)
    return app
