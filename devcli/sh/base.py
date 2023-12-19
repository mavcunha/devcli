import logging
import os
import shlex
import subprocess
import sys
from subprocess import CompletedProcess
from typing import Any, Union, List


def _quote_command(command):
    quoted_command = shlex.quote(command)
    # attempt to use user's shell, fallback to /bin/sh
    user_shell = os.environ.get('SHELL', '/bin/sh')
    final_command = f"{user_shell} -c {quoted_command}"
    return final_command


def _stdout_exec(command: str):
    logging.info(f'run:{command}')
    final_command = _quote_command(command)
    logging.debug(f'final_command: {final_command}')
    proc = subprocess.Popen(final_command, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            env=os.environ,
                            text=True)
    for line in proc.stdout:
        sys.stdout.write(line)
    proc.wait()
    return proc.returncode


def run(command: Union[str, List[str]]):
    """
    A basic shell execution that will execute the command and directly
    output its messages.
    It won't capture the output and calling this
    is a run and forget.
    If a list of commands is given it will attempt to execute each one
    in order and will stop as soon a command fails.
    Similar to what `cmd1 && cmd2 && cmd3` would do in shell.
    """
    if isinstance(command, list):
        for c in command:
            result = _stdout_exec(c)
            if result != 0:
                logging.info(f"'{c}' failed.")
                break
    elif isinstance(command, str):
        return _stdout_exec(command)
    else:
        raise ValueError(f"{command} is not str or List[str]")


def capture(command: str) -> str:
    """
    A run which captures the output and returns it, it won't display the stdout
    of the command during its execution.
    """
    logging.debug(f'running shell: {command}')
    final_command = _quote_command(command)
    result = subprocess.run(final_command, shell=True, capture_output=True, text=True)
    logging.debug(f'return code: {result.returncode}')
    return result.stdout


class ShellExecutable:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.result = None

    def capture(self, cmd: str):
        self.result = capture(cmd)
        return self.result
