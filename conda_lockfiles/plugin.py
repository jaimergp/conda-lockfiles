from __future__ import annotations

from conda import plugins

from . import cli


@plugins.hookimpl
def conda_subcommands():
    yield plugins.CondaSubcommand(
        name="lockfiles",
        summary="Create new environments from different conda ecosystem lockfiles",
        action=cli.execute,
        configure_parser=cli.configure_parser,
    )
