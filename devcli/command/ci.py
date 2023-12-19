from devcli import cmd

from typer import Context

cli = cmd.cli("General CI command line")


@cli.command()
def status(ctx: Context, job: str):
    cmd.echo(f'CI status')

