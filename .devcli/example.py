from devcli import cmd

cli = cmd.cli("Simplest example of creating a command")


@cli.command()
def test():
    """Example command"""
    cmd.echo("Example command")


@cli.command()
def ping():
    cmd.echo('[green]PONG![/green]')
