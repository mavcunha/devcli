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
    """
    Show devcli version
    :return:
    """
    project_conf = Config().add_config(project_root('pyproject.toml'))
    print(f'devcli version {project_conf['tool.poetry.version']}')


@cli.callback(invoke_without_command=True)
def main(ctx: Context,
         debug: bool = typer.Option(False, "--debug", help="Enable debug log"),
         verbose: bool = typer.Option(False, "--verbose", help="Enable info log")):
    logger = logging.getLogger()
    if debug:
        logger.setLevel(level=logging.DEBUG)
        logging.debug("Debug logging enabled")
    elif verbose:
        logger.setLevel(level=logging.INFO)
        logging.info("Verbose mode enabled")

    # call help on the absense of a command
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()

    ctx.obj = Config()
