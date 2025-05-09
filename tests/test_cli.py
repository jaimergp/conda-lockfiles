from __future__ import annotations

from typing import TYPE_CHECKING

from conda_lockfiles import APP_NAME, APP_VERSION

if TYPE_CHECKING:
    from conda.testing.fixtures import CondaCLIFixture


def test_help(conda_cli: CondaCLIFixture) -> None:
    _, _, exception = conda_cli("lockfiles", "--help", raises=SystemExit)
    assert exception.value.code == 0


def test_version(conda_cli: CondaCLIFixture) -> None:
    stdout, _, exception = conda_cli("lockfiles", "--version", raises=SystemExit)
    assert f"{APP_NAME} {APP_VERSION}" == stdout.strip()
    assert exception.value.code == 0


def test_create_help(conda_cli: CondaCLIFixture) -> None:
    _, _, exception = conda_cli("lockfiles", "create", "--help", raises=SystemExit)
    assert exception.value.code == 0


def test_export_help(conda_cli: CondaCLIFixture) -> None:
    _, _, exception = conda_cli("lockfiles", "export", "--help", raises=SystemExit)
    assert exception.value.code == 0
