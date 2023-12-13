import click
import toml

from devcli import config_path

CONFIG = None


def msg(m: str) -> None:
    click.echo(m)


def warn(m: str) -> None:
    click.secho(m, fg="yellow")


def error(m: str) -> None:
    click.secho(m, fg="red")


def config():
    global CONFIG
    if CONFIG is None:
        CONFIG = toml.load(config_path("devcli.toml"))
    return CONFIG
