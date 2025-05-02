"""
conda lockfiles-from-env subcommand for CLI
"""

from __future__ import annotations

import argparse


def configure_parser(parser: argparse.ArgumentParser):
    from conda.base.context import context
    from conda.cli.conda_argparse import add_parser_help
    from conda.cli.helpers import add_parser_prefix

    from .export_env import LOCKFILE_FORMATS

    parser.prog = "conda lockfiles-from-env"
    add_parser_prefix(parser, True)
    add_parser_help(parser)
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
    )


def execute(args: argparse.Namespace) -> int:
    from conda.base.context import context, determine_target_prefix
    from .export_env import export_env_to_lockfile

    prefix = determine_target_prefix(context, args)
    export_env_to_lockfile(args.lockfile_format, prefix, args.lockfile_path)
    return 0
