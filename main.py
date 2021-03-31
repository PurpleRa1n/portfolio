#!/usr/bin/env python3
from pathlib import Path

import click
from aiohttp import web
from alembic.command import upgrade

from core import settings
from core.app import create_app
from core.database.utils import get_database_dsn, alembic_config_from_url

CURRENT_DIR = Path(__file__).parent


@click.group()
def main():
    """
    Usage: ./main.py COMMAND [ARG...]

    Commands:

        runserver   Start a web service
        migrate   Migrate database

    Example:\n
        >>> ./main.py runserver
        >>> ./main.py migrate
    """


@click.command()
def runserver() -> None:
    """
    Runs a web service
    """
    click.echo("runs an application ...")
    app = create_app()
    web.run_app(app, host=settings.APP_HOST, port=settings.APP_PORT)


@click.command()
def migrate() -> None:
    alembic_config = alembic_config_from_url(get_database_dsn(is_migration=True))
    upgrade(alembic_config, 'head')


main.add_command(runserver)
main.add_command(migrate)

if __name__ == "__main__":
    main()
