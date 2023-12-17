import logging
import os.path
from pathlib import Path
from typing import Any

import toml

from devcli import project_root


class Config:

    logger = logging.getLogger(__name__)

    def __init__(self, config_file=None):
        self._config = {}
        if config_file:
            self.add_config(config_file)

    def add_config(self, config_file) -> None:
        if os.path.isfile(config_file):
            with open(config_file) as file:
                self.logger.debug(f'loading {config_file} data')
                self._config.update(toml.load(file))
        else:
            self.logger.warning(f'{config_file} is not a file or does not exist')

    def __getitem__(self, item) -> Any:
        return self._config.get(item, None)

    def __repr__(self):
        return toml.dumps(self._config)

    @staticmethod
    def find_config_files(filename: str | Path, start_dir: str | Path = Path.cwd()) -> [str]:
        config_paths = []
        current_dir = Path(start_dir)

        # Traverse up the directory tree
        while True:
            config_path = current_dir / filename
            if config_path.exists():
                config_paths.append(str(config_path))

            if current_dir.parent == current_dir:  # Root directory reached
                break
            current_dir = current_dir.parent

        return config_paths

    @classmethod
    def load(cls):
        cls.logger.debug('loading configurations')
        config_instance = cls()

        # load defaults
        config_instance.add_config(Path(project_root()) / "conf" / "defaults.toml")

        # home dir configurations
        config_instance.add_config(Path.home() / ".config" / "devcli" / "conf.toml")

        # standard up dir transversal looking for configuration files
        for config_file in reversed(cls.find_config_files('devcli.toml')):
            config_instance.add_config(config_file)

        return config_instance
