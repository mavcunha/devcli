from .basic import get_cli, echo
from .config import Config

conf = Config()

__all__ = ["get_cli", "echo", "conf"]
