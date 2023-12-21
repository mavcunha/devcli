from .basic import cli, echo, error, warn, stop, notice
from .config import Config

conf = Config()

# Functions related to print messages back to the user
_msg = ['echo', 'error', 'warn', 'notice']

__all__ = ["cli", "conf", "stop"] + _msg
