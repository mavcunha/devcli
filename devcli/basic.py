"""
devcli.command is a collection of helper functions for tool commands
so that they don't have to reimplement common tasks related to a command
work.
"""

import typer
from rich import print as rich_print


def get_cli() -> typer.Typer:
    """
    The base of starting a new dynamic command. It
    returns the basic Typer type for command declaration.
    :returns: a typer.Typer
    """
    return typer.Typer()


def echo(*args, **kwargs):
    r"""
    Copied from rich.print(). Print object(s) supplied via positional arguments.
    This function has an identical signature to the built-in print.
    For more advanced features, see the :class:`~rich.console.Console` class.

    Args:
        sep (str, optional): Separator between printed objects. Defaults to " ".
        end (str, optional): Character to write at end of output. Defaults to "\\n".
        file (IO[str], optional): File to write to, or None for stdout. Defaults to None.
        flush (bool, optional): Has no effect as Rich always flushes output. Defaults to False.

    """
    rich_print(*args, **kwargs)
