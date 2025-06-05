from __future__ import annotations

from typing import TYPE_CHECKING

from conda_lockfiles.loaders.explicit import ExplicitLoader

from .. import EXPLICIT_LOCK_DIR

if TYPE_CHECKING:
    from pathlib import Path


def test_explicit_loader_supports(tmp_path: Path) -> None:
    assert ExplicitLoader.supports(EXPLICIT_LOCK_DIR / "explicit.txt")
    assert not ExplicitLoader.supports(EXPLICIT_LOCK_DIR / "not_explicit.txt")
    assert not ExplicitLoader.supports(tmp_path / "explicit.txt")
    assert not ExplicitLoader.supports(tmp_path / "not_explicit.txt")


def test_explicit_loader_load() -> None:
    loader = ExplicitLoader(EXPLICIT_LOCK_DIR / "explicit.txt")
    assert "@EXPLICIT" in loader.data
