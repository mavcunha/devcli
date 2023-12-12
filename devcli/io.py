import click
import toml

import devcli.cli
from devcli import config_path

CONFIG = None


def print_message(m: str) -> None:
    click.echo(m)


def warn(m: str) -> None:
    click.secho(m, fg="yellow")


def error(m: str) -> None:
    click.secho(m, fg="red")


def config():
    global CONFIG
    if CONFIG is None:
        CONFIG = parse_config(config_path("devcli.toml"))
    return CONFIG


def parse_config(config_file):
    return toml.load(config_file)
