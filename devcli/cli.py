import logging
import pathlib

import typer
from typer import Context
from rich import print

from devcli import project_root, load_dynamic_commands, load_default_commands
from devcli.config import Config

cli = typer.Typer()

load_default_commands(cli)
load_dynamic_commands(cli, pathlib.Path('.devcli'))


@cli.command()
def version():
    project_conf = Config(project_root('pyproject.toml'))
    print(f'devcli version {project_conf['tool']['poetry']['version']}')


@cli.callback(invoke_without_command=True)
def main(ctx: Context, debug: bool = typer.Option(False, "--debug", help="Enable debug log")):
    if debug:
        logging.getLogger().setLevel(level=logging.DEBUG)
        logging.debug("Debug logging enabled")

    # call help on the absense of a command
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()

    ctx.obj = Config.load()
