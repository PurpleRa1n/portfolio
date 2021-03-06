import asyncio
import pathlib
from typing import Dict

import uvloop
from aiohttp import web
from aiohttp.web_app import Application
from yarl import URL

from auth.routes import routes
from tic_tac_toe.routes import routes as ttt_routes
from core import settings
from core.database.orm import db
from core.database.utils import get_gino_database_config, get_database_name
from core.utils.module_loading import import_string
from core.views import HealthCheckView

PROJ_ROOT = pathlib.Path(__file__).parent.parent

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def _init_db(app: Application, database_url: str = None) -> Application:
    """
    Initialize gino orm.
    """
    db_name = URL(database_url).name if database_url is not None else get_database_name()
    db_config: Dict = get_gino_database_config(db_name)
    db.init_app(app=app, config=db_config)
    return app


def _create_app() -> Application:
    """
    Returns web application instance.
    """
    app: Application = web.Application()
    return app


def _init_middlewares(app: Application) -> Application:
    """
    Load middleware logic and attach it to the application
    """
    app.middlewares.extend([import_string(path) for path in settings.MIDDLEWARES])
    return app


def _init_routes(app: Application) -> Application:
    """
    Initialize all application routes
    """
    for module_routes in [routes, ttt_routes]:
        for method, route, handler in module_routes:
            app.router.add_route(method, route, handler)
    app.router.add_view('/health-check/', HealthCheckView)
    return app


def create_app(database_dsn: str = None) -> Application:
    """
    The main entry point for creating a web application and configuring it.
    """
    app: Application = _create_app()
    app = _init_db(app, database_url=database_dsn)
    app = _init_routes(app)
    app = _init_middlewares(app)
    return app
