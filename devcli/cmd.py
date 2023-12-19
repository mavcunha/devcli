from .basic import cli, echo, error
from .config import Config

conf = Config()

__all__ = ["cli", "echo", "error", "conf"]
