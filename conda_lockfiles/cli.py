"""
conda lockfiles subcommand for CLI
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def configure_parser(parser: argparse.ArgumentParser):
    from conda.base.context import context
    from conda.cli.conda_argparse import add_parser_help
    from conda.cli.helpers import add_parser_prefix

    parser.prog = "conda lockfiles"
    add_parser_prefix(parser, True)
    add_parser_help(parser)
    parser.add_argument("path", help="Path to pixi.lock file")
    parser.add_argument(
        "-e", "--environment", default="default", help="Environment name in lockfile"
    )
    parser.add_argument(
        "-s",
        "--subdir",
        "--platform",
        dest="platform",
        default=context.subdir,
        help="Target platform",
    )


def execute(args: argparse.Namespace) -> int:
    from conda.base.context import context, determine_target_prefix

    from .create import create_environment_from_lockfile

    prefix = determine_target_prefix(context, args)
    create_environment_from_lockfile(
        lockfile=args.path,
        prefix=prefix,
        environment=args.environment,
        platform=args.platform,
    )
    return 0
