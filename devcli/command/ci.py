from devcli import cmd

cli = cmd.get_cli()


@cli.command()
def status(job: str):
    cmd.echo("job status")
