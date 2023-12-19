from devcli import cmd
from devcli.sh.one_password import OnePassword
from devcli.utils import MissConfError

cli = cmd.cli("Shortcuts for 1Password CLI")


def get_op():
    acct = cmd.conf['devcli.secret.op.account']
    vault = cmd.conf['devcli.secret.op.vault']
    if acct is None:
        raise MissConfError(topic="devcli.secret.op", entry="account", example="VALID_OP_ACCOUNT")
    return OnePassword(acct, vault=vault)


@cli.command()
def credential(key: str):
    """
    Will read from 1Password an entry in the form op://Private/{key}/credential
    """
    cmd.echo(get_op().credential(key))


@cli.command()
def password(item: str):
    """
    Will read from 1Password an login entry and return its password
    """
    cmd.echo(get_op().password(item))
