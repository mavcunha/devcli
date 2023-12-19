from devcli import cmd
from typer import Context

cli = cmd.cli("Collections of command templates for reference")


@cli.command()
def hello(name: str):
    """
    Example of a simple command that takes one string argument
    """
    cmd.echo(f"Hello {name}!")


@cli.command()
def config(ctx: Context):
    """
    Example of access to global configurations
    """
    cmd.echo(f"Default config: {ctx.obj['devcli']}")


@cli.command()
def version():
    """
    Example of a command that calls a function on devcli
    """
    import devcli.cli
    devcli.cli.version()


@cli.command()
def goodbye(name: str, formal: bool = False):
    """
    Example of a command with an optional flag
    """
    if formal:
        cmd.echo(f"Goodbye, Ms. {name}. Have a good day!")
    else:
        cmd.echo(f"Bye, [yellow]{name}[/yellow]!")


@cli.command()
def ping():
    cmd.echo('[green]PONG![/green]')
