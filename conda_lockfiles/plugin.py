from __future__ import annotations

from conda import plugins

from . import cli
from . import from_env


@plugins.hookimpl
def conda_subcommands():
    yield plugins.CondaSubcommand(
        name="lockfiles",
        summary="Create new environments from different conda ecosystem lockfiles",
        action=cli.execute,
        configure_parser=cli.configure_parser,
    )
    yield plugins.CondaSubcommand(
        name="lockfiles-from-env",
        summary="Create a lockfile from an existing enviromment",
        action=from_env.execute,
        configure_parser=from_env.configure_parser,
    )
