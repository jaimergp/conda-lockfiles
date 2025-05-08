from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def configure_parser(parser: argparse.ArgumentParser) -> None:
    from .. import APP_NAME, APP_VERSION
    from .main_create import HELP as CREATE_HELP
    from .main_create import configure_parser as configure_parser_create
    from .main_export import HELP as EXPORT_HELP
    from .main_export import configure_parser as configure_parser_export

    # conda lockfiles --version
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"{APP_NAME} {APP_VERSION}",
        help=f"Show the {APP_NAME} version number and exit.",
    )

    subparsers = parser.add_subparsers(
        title="subcommands",
        dest="subcommand",
        required=True,
    )

    configure_parser_create(subparsers.add_parser("create", help=CREATE_HELP))
    configure_parser_export(subparsers.add_parser("export", help=EXPORT_HELP))


def execute(args: argparse.Namespace) -> int:
    return args.func(args)
