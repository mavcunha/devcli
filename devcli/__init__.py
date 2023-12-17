import importlib.util
import logging
import os
import pathlib

from typer import Typer

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

DEVCLI_LOGLEVEL = os.environ.get('DEVCLI_LOGLEVEL', "WARNING")

logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.getLevelName(DEVCLI_LOGLEVEL.upper()))

# debug only available if DEVCLI_LOGLEVEL is defined as "debug"
_init_logger = logging.getLogger('devcli.__init__')


# generic get this project root path
def project_root(filename=None):
    parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if filename is None:
        return parent
    else:
        return os.path.join(parent, filename)


def load_dynamic_commands(app: Typer, directory: pathlib.Path):
    if not directory.exists():
        _init_logger.debug(f"couldn't find dir {directory}")
        return

    for file in directory.glob("*.py"):
        _init_logger.debug(f"found file: {file}")
        module_name = file.stem  # Get the file name without '.py'
        _init_logger.debug(f'module: {module_name}')
        spec = importlib.util.spec_from_file_location(module_name, file)
        module = importlib.util.module_from_spec(spec)
        _init_logger.debug(f'executing module: {module}')
        spec.loader.exec_module(module)
        if hasattr(module, 'cli'):
            _init_logger.debug(f'"cli" attribute found, adding command: {module_name}')
            app.add_typer(module.cli, name=module_name)


def load_default_commands(cli: Typer) -> None:
    """
    This function is in charge of loading the default commands for devcli.
    We don't use the dynamic loading in this case to save time and control
    which ones should be loaded or not.

    The command will be defined as its name, for example 'devcli.command.ci' will
    be defined as 'ci'

    :param cli: a Typer object that allow for `.add_typer` calls
    :return: None
    """
    # default commands that can be reused
    from devcli.command import (
        ci,
        op,
    )
    commands = [ci, op]
    for c in commands:
        _init_logger.debug(f'loading default command ({c.__name__})')
        cli.add_typer(c.cli, name=c.__name__.split('.')[-1])
