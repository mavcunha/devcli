from devcli import cmd

cli = cmd.cli("Simplest example of creating a command")


@cli.command()
def test():
    """Example command"""
    cmd.echo("Example command")


@cli.command()
def ping():
    cmd.echo('[green]PONG![/green]')


@cli.command()
def text():
    """Demo types of text output you can use"""
    cmd.echo('This is cmd.echo(msg)')
    cmd.notice('This is cmd.notice(msg)')
    cmd.warn('This is cmd.warn(msg)')
    cmd.error('This is cmd.error(msg)')

