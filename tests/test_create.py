from __future__ import annotations

import json
from typing import TYPE_CHECKING

from conda_lockfiles.create import create_environment_from_lockfile

from . import PIXI_METADATA_DIR

if TYPE_CHECKING:
    from pathlib import Path


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
