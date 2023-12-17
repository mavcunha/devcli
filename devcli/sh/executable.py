import logging
import subprocess


class ShellExecutable:
    logger = logging.getLogger(__name__)

    def run(self, executable: 'ShellExecutable') -> str:
        command = str(executable)
        self.logger.debug(f'running shell: {command}')
        result = subprocess.run(str(executable), shell=True, capture_output=True, text=True)
        self.logger.debug(f'return code: {result.returncode}')
        return result.stdout
