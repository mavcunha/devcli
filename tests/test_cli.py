import re
from typer.testing import CliRunner
from devcli.cli import cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli, ['version'])
    assert re.match(r".*\d+\.\d+\.\d+$", result.output) is not None
