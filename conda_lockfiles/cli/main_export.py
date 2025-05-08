"""
conda lockfiles export subcommand for CLI
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

HELP = "Export a conda environment to a lock file."


def configure_parser(parser: argparse.ArgumentParser):
    from conda.cli.helpers import add_parser_prefix

    from ..export import LOCKFILE_FORMATS

    parser.description = HELP

    add_parser_prefix(parser, True)
    parser.add_argument(
        "-f",
        "--file",
        metavar="PATH",
        dest="lockfile_path",
        help="Path to save lockfile, if not specified output to stdout.",
    )
    parser.add_argument(
        "--format",
        dest="lockfile_format",
        choices=LOCKFILE_FORMATS.keys(),
        help="Lockfile format to create.",
        required=True,
    )
    parser.set_defaults(func=execute)


def execute(args: argparse.Namespace) -> int:
    from conda.base.context import context

    from ..export import export_environment_to_lockfile

    export_environment_to_lockfile(
        args.lockfile_format,
        context.target_prefix,
        args.lockfile_path,
    )
    return 0
