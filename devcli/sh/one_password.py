import logging

from devcli.sh.executable import ShellExecutable


class OnePassword(ShellExecutable):
    logger = logging.getLogger(__name__)

    def __init__(self, account: str):
        self.account = f'--account {account}'

    def read(self, key: str) -> str:
        return self.run(f'op read {self.account} op://{key}').stdout.rstrip('\n')

    def credential(self, key: str) -> str:
        return self.read(f'Private/{key}/credential')

    def password(self, item: str) -> str:
        return self.read(f'Private/{item}/password')
