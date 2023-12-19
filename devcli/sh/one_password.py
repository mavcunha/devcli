import logging

from devcli.sh.base import ShellExecutable, capture


class OnePassword(ShellExecutable):
    logger = logging.getLogger(__name__)

    def __init__(self, account: str, vault: str = 'Private'):
        super().__init__()
        self.logger.debug(f'using account:{account} and vault:{vault}')
        self.account = f'--account {account}'
        self.vault = vault

    def read(self, key: str) -> str:
        self.logger.debug(f'read key={key}')
        return capture(f'op read {self.account} op://{key}').rstrip('\n')

    def credential(self, key: str) -> str:
        return self.read(f'{self.vault}/{key}/credential')

    def password(self, item: str) -> str:
        return self.read(f'{self.vault}/{item}/password')

    def login(self, item: str) -> str:
        return self.read(f'{self.vault}/{item}/login')
