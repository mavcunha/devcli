import logging
import os
import random
import shlex
import subprocess
import threading
from typing import Union, List

from devcli.utils import styled_text


def _prepare_command(command):
    quoted_command = shlex.quote(command)
    # attempt to use user's shell, fallback to /bin/sh
    user_shell = os.environ.get('SHELL', '/bin/sh')
    final_command = f"{user_shell} -c {quoted_command}"
    return final_command


def create_process(command: str):
    logging.info(f'run:{command}')
    final_command = _prepare_command(command)
    logging.debug(f'final_command: {final_command}')
    proc = subprocess.Popen(final_command, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            env=os.environ,
                            bufsize=1,
                            universal_newlines=True,
                            text=True)
    return proc


def process_output(process, process_name: str):
    while True:
        output = process.stdout.readline()
        if process.poll() is not None and output == '':
            break
        if output:
            print(f"{process_name}: {output.strip()}")


def start_process_thread(process, alias):
    thread = threading.Thread(target=process_output,
                              args=(process, alias))
    thread.start()
    return thread


def iter_for(commands):
    """
    Will return an iterable in the form of k,v for
    any str in a list, dict or purely a str
    """
    if isinstance(commands, list):
        return enumerate(list)
    elif isinstance(commands, dict):
        return commands.items()
    else:
        # since commands is a single command, split any arguments
        # and get the command name as its own alias
        alias = os.path.basename(commands.split(' ')[0])
        return iter_for({alias: commands})


def run(command: Union[str, List[str], dict]):
    """
    A basic shell execution that will execute the command and directly
    output its messages.
    It won't capture the output and calling this is a run and forget.
    If a list of commands is given it will attempt to execute each one
    in order and will stop as soon a command fails.
    Similar to what `cmd1 && cmd2 && cmd3` would do in shell.
    """
    procs = []
    for alias, cmd in iter_for(command):
        process = create_process(cmd)
        thread = start_process_thread(process, styled_text(f"{alias}", f'color({random.randint(1, 231)})'))
        procs.append((process, thread))
    for proc, thread in procs:
        proc.wait()
        thread.join()


def capture(command: str) -> str:
    """
    A run which captures the output and returns it, it won't display the stdout
    of the command during its execution.
    """
    logging.debug(f'running shell: {command}')
    final_command = _prepare_command(command)
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
