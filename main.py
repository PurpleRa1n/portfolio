#!/usr/bin/env python3
from pathlib import Path

import click
from aiohttp import web

from core import settings
from core.app import create_app

CURRENT_DIR = Path(__file__).parent


@click.group()
def main():
    """
    Usage: ./main.py COMMAND [ARG...]

    Commands:

        runserver   Start a web service

    Example:\n
        >>> ./main.py runserver
    """


@click.command()
def runserver() -> None:
    """
    Runs a web service
    """
    click.echo("runs an application ...")
    app = create_app()
    web.run_app(app, host=settings.APP_HOST, port=settings.APP_PORT)


main.add_command(runserver)

if __name__ == "__main__":
    main()
