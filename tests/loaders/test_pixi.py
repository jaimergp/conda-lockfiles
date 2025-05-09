from __future__ import annotations

from typing import TYPE_CHECKING

from conda_lockfiles.loaders.pixi import PixiLoader

from .. import PIXI_DIR

if TYPE_CHECKING:
    from pathlib import Path

    from pytest import MockerFixture


def test_pixi_loader_supports(mocker: MockerFixture, tmp_path: Path) -> None:
    assert PixiLoader.supports(PIXI_DIR / "pixi.lock")
    assert not PixiLoader.supports(PIXI_DIR / "pixi.toml")
    assert not PixiLoader.supports(tmp_path / "pixi.lock")
    assert not PixiLoader.supports(tmp_path / "pixi.toml")


def test_pixi_loader_load() -> None:
    loader = PixiLoader(PIXI_DIR / "pixi.lock")
    assert loader.data["version"] == 6
    assert len(loader.data["environments"]["default"]["packages"]["noarch"]) == 2
