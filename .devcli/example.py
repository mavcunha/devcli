from devcli import cmd

cli = cmd.get_cli()


@cli.command()
def test():
    """Example command"""
    cmd.echo("Example command")


@cli.command()
def ping():
    cmd.echo('[green]PONG![/green]')
