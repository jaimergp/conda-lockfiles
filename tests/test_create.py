from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest
from conda.common.compat import on_win
from conda.models.match_spec import MatchSpec

from conda_lockfiles.create import (
    create_environment_from_lockfile,
    lookup_conda_records,
)
from conda_lockfiles.loaders.conda_lock_v1 import CONDA_LOCK_FILE

from . import (
    CONDA_LOCK_METADATA_DIR,
    EXPLICIT_LOCK_DIR,
    PIXI_METADATA_DIR,
)

if TYPE_CHECKING:
    from pathlib import Path

    from conda_lockfiles.loaders.base import PackageRecordOverrides


def test_create_environment_from_lockfile_pixi_metadata(tmp_path: Path) -> None:
    create_environment_from_lockfile(
        PIXI_METADATA_DIR / "pixi.lock",
        tmp_path,
        environment="default",
        platform="linux-64",
    )
    env_record_path = tmp_path / "conda-meta" / "tzdata-2025b-h78e105d_0.json"
    assert env_record_path.is_file()
    data = json.loads(env_record_path.read_bytes())
    assert data["license"] == "ONLY_IN_LOCKFILE"


@pytest.mark.skipif(
    condition=on_win,
    reason="linux environment creation is not supported on Windows",
)
def test_create_environment_from_lockfile_conda_lock_metadata(tmp_path: Path) -> None:
    create_environment_from_lockfile(
        CONDA_LOCK_METADATA_DIR / CONDA_LOCK_FILE,
        tmp_path,
        platform="linux-64",
    )
    env_record_path = tmp_path / "conda-meta" / "libsqlite-3.50.0-hee588c1_0.json"
    assert env_record_path.is_file()
    data = json.loads(env_record_path.read_bytes())
    # package/repodata has .<2.0a0
    assert "libzlib >=1.3.1,<2.0a1" in data["depends"]


def test_create_environment_from_explicit_file(tmp_path: Path) -> None:
    create_environment_from_lockfile(
        EXPLICIT_LOCK_DIR / "explicit.txt",
        tmp_path,
        platform="linux-64",
    )
    env_record_path = tmp_path / "conda-meta" / "tzdata-2025b-h04d1e81_0.json"
    assert env_record_path.is_file()
    data = json.loads(env_record_path.read_bytes())
    assert (
        data["sha256"]
        == "3c9fefdfb2335e8641642e964cfaf20513d40ec709ab559b47b52d99b2e46fea"
    )


def test_lookup_conda_records(tmp_path: Path) -> None:
    md5 = "4222072737ccff51314b5ece9c7d6f5a"
    sha256 = "5aaa366385d716557e365f0a4e9c3fca43ba196872abbbe3d56bb610d131e192"
    spec = MatchSpec(
        "https://conda.anaconda.org/conda-forge/noarch/tzdata-2025b-h78e105d_0.conda",
        md5=md5,
        sha256=sha256,
    )
    license = "ONLY_IN_TEST"
    overrides: PackageRecordOverrides = {"license": license}

    records = lookup_conda_records({spec: overrides})
    assert isinstance(records, tuple)
    assert len(records) == 1
    record = records[0]
    assert record.name == "tzdata"
    # set by match spec
    assert record.md5 == md5
    assert record.sha256 == sha256
    # set by overrides
    assert record.license == license
    # only known after downloading
    assert record.size == 122_968
