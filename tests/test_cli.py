import re
from click.testing import CliRunner
from devcli.cli import cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli, ['version'])
    assert re.match(r".*\d+\.\d+\.\d+$", result.output) is not None


def test_command_not_found():
    result = runner.invoke(cli, ['not-found'])
    assert result.exit_code == 0

