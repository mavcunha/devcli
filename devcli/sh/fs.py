from pathlib import Path
from typing import Union


def file_exists(path: Union[Path, str]) -> bool:
    """
    Simple shortcut to check file existence
    """
    path = _ensure_its_path(path)
    return path.is_file() and path.exists()


def dir_exists(path: Union[Path, str]) -> bool:
    """
    Simple shortcut to check directory existence
    """
    path = _ensure_its_path(path)
    return path.is_dir() and path.exists()


def _ensure_its_path(path):
    if type(path) is str:
        path = Path(path)
    return path
