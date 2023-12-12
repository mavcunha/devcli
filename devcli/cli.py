import shlex
import subprocess
import typing as t

import click
import toml
from click import Context, Command

import devcli.io
from devcli import project_root
import devcli.io as io


def execute_fallback(cmd_name, args):
    args = ' '.join(shlex.quote(str(arg)) for arg in args)
    full_command = f"{io.config()['devcli']['fallback_command']} {cmd_name} {args}"
    io.warn(f"Executing fallback command: {full_command}")
    return subprocess.run(full_command, shell=True).returncode


class MyCLI(click.Group):

    def get_command(self, ctx: Context, cmd_name: str) -> t.Optional[Command]:
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        # Fallback command handler
        def fallback_command(args):
            execute_fallback(cmd_name, args)

        return click.Command(cmd_name,
                             context_settings=dict(ignore_unknown_options=True),
                             params=[click.Argument(['args'], nargs=-1)], callback=fallback_command)


@click.group(cls=MyCLI)
def cli():
    devcli.io.CONFIG = io.config()
    pass


@cli.command(help="Show version information")
def version():
    # set version as pyproject.toml is defined
    with open(project_root("pyproject.toml")) as file:
        project_info = toml.load(file)
        version_number = project_info.get("tool", {}).get("poetry", {}).get("version", "")
    return io.print_message(f"devcli: v{version_number}")


@cli.command(help="Call fallback command", context_settings=dict(ignore_unknown_options=True))
@click.argument('args', nargs=-1)
def fallback(args):
    if len(args) == 0:
        execute_fallback('', [])
    else:
        execute_fallback(args[0], args[1:])
