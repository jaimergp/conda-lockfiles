from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from conda.testing.fixtures import CondaCLIFixture


def test_help(conda_cli: CondaCLIFixture) -> None:
    conda_cli("lockfiles", "--help", raises=SystemExit)


def test_version(conda_cli: CondaCLIFixture) -> None:
    conda_cli("lockfiles", "--version", raises=SystemExit)


def test_create_help(conda_cli: CondaCLIFixture) -> None:
    conda_cli("lockfiles", "create", "--help", raises=SystemExit)
