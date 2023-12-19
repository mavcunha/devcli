"""
devcli.command is a collection of helper functions for tool commands
so that they don't have to reimplement common tasks related to a command
work.
"""
import sys

import typer
from rich import print as rich_print


def cli(description: str = None) -> typer.Typer:
    """
    The base of starting a new dynamic command. It
    returns the basic Typer type for command declaration.
    :returns: a typer.Typer
    """
    return typer.Typer(help=description)


def echo(msg: str):
    rich_print(msg)


def error(msg: str):
    rich_print(f"[red]{msg}[/red]")
    sys.exit(1)
