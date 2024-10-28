from .sh.base import run, capture
from .sh.fs import file_exists, dir_exists

# file system operations
fs = ['file_exists', 'dir_exists']
# base shell operations
base = ['run', 'capture']

__all__ = base + fs
