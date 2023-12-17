import logging

from devcli import cmd
from devcli.sh.executable import ShellExecutable


class OnePassword(ShellExecutable):

    logger = logging.getLogger(__name__)

    def __init__(self, account: str):
        self._cmd = None
        self._item = None
        self.account = account

    def get(self, key: str) -> str:
        self.logger.info("something")

    def credential(self, key: str):
        self._cmd = 'read'
        self._item = f'Private/{key}/credential'
        return self.run(self)

    def __repr__(self):
        return f'op {self._cmd} --account {self.account} op://{self._item}'



cli = cmd.get_cli()


@cli.command()
def get(key: str):
    account_ = cmd.conf['devcli.secret.op.account']
    op = OnePassword(account_)
    p = op.credential('jenkins')
    cmd.echo(f"reading secret {p}")
