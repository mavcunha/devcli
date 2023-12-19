import logging
import os.path
from pathlib import Path
from typing import Any

import toml

from devcli import project_root


class Config:
    logger = logging.getLogger(__name__)
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls.logger.debug(f'loading Config')

            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)

            cls._instance._config = {}  # init config holder empty

            # load defaults
            cls._instance.add_config(Path(project_root()) / "conf" / "defaults.toml")

            # home dir configurations
            cls._instance.add_config(Path.home() / ".config" / "devcli" / "conf.toml")

            # standard up dir transversal looking for configuration files
            for config_file in reversed(cls.find_config_files('devcli.toml')):
                cls._instance.add_config(config_file)

        return cls._instance

    def add_config(self, config_file):
        if os.path.isfile(config_file):
            with open(config_file) as file:
                self.logger.debug(f'loading {config_file} data')
                self._config.update(toml.load(file))
        else:
            self.logger.warning(f'{config_file} is not a file or does not exist')

        return self

    def __getitem__(self, item: str) -> Any:
        self.logger.debug(f'getitem:{item}')
        if "." in item:
            keys = item.split('.')
            level = self._config
            for key in keys:
                if isinstance(level, dict) and key in level:
                    level = level[key]
                else:
                    return None
            return level
        else:
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
