from devcli import cmd
from devcli.sh.one_password import OnePassword
from devcli.utils import MissConfError

cli = cmd.get_cli()


def get_op():
    acct = cmd.conf['devcli.secret.op.account']
    if acct is None:
        raise MissConfError(topic="devcli.secret.op", entry="account", example="VALID_OP_ACCOUNT")
    return OnePassword(acct)


@cli.command()
def credential(key: str):
    cmd.echo(get_op().credential(key))


@cli.command()
def password(item: str):
    cmd.echo(get_op().password(item))
