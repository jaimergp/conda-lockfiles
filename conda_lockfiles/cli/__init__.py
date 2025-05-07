from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def configure_parser(parser: argparse.ArgumentParser) -> None:
    from .main_create import configure_parser as configure_parser_create
    from .main_export import configure_parser as configure_parser_export

    subparsers = parser.add_subparsers(
        title="subcommand",
        description="The following subcommands are available.",
        dest="cmd",
        required=True,
    )

    configure_parser_create(subparsers.add_parser("create"))
    configure_parser_export(subparsers.add_parser("export"))


def execute(args: argparse.Namespace) -> int:
    return 0
