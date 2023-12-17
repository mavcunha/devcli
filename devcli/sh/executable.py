import logging
import subprocess
from subprocess import CompletedProcess
from typing import Any


class ShellExecutable:
    logger = logging.getLogger(__name__)

    def run(self, command: str) -> CompletedProcess[str] | CompletedProcess[Any]:
        self.logger.debug(f'running shell: {command}')
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        self.logger.debug(f'return code: {result.returncode}')
        return result
