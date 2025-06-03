from __future__ import annotations

from typing import TYPE_CHECKING

from conda_lockfiles.loaders.conda_lock_v1 import CondaLockV1Loader

from .. import CONDA_LOCK_METADATA_DIR

if TYPE_CHECKING:
    from pathlib import Path


def test_conda_lock_v1_loader_supports(tmp_path: Path) -> None:
    assert CondaLockV1Loader.supports(CONDA_LOCK_METADATA_DIR / "conda-lock.yml")
    assert not CondaLockV1Loader.supports(CONDA_LOCK_METADATA_DIR / "environment.yaml")
    assert not CondaLockV1Loader.supports(tmp_path / "conda-lock.yml")
    assert not CondaLockV1Loader.supports(tmp_path / "environment.yaml")


def test_conda_lock_v1_loader_load() -> None:
    loader = CondaLockV1Loader(CONDA_LOCK_METADATA_DIR / "conda-lock.yml")
    assert loader.data["version"] == 1
    assert len(loader.data["package"]) == 14
