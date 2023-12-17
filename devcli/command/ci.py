from devcli import cmd

from typer import Context

cli = cmd.get_cli()


@cli.command()
def status(ctx: Context, job: str):
    cmd.echo(f'CI status')

