from unittest import mock

from devcli.io import msg, warn, error


def test_simple_output():
    with mock.patch("click.echo") as echo:
        msg("Hello World!")
        echo.assert_called_with("Hello World!")


def test_simple_error():
    with mock.patch("click.secho") as echo:
        warn("This is a warning!")
        echo.assert_called_with("This is a warning!", fg="yellow")


def test_error():
    with mock.patch("click.secho") as echo:
        error("This is a error!")
        echo.assert_called_with("This is a error!", fg="red")
