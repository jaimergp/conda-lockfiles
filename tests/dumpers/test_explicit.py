from __future__ import annotations

from typing import TYPE_CHECKING

from conda_lockfiles.dumpers import explicit

from .. import SINGLE_PACKAGE_ENV

if TYPE_CHECKING:
    from pathlib import Path


def test_export_to_explicit(tmp_path: Path) -> None:
    lockfile_path = tmp_path / "explicit.txt"
    explicit.export_to_explicit(str(SINGLE_PACKAGE_ENV), str(lockfile_path))
    assert lockfile_path.exists()
    data = lockfile_path.read_text()
    assert "specs: python_abi" in data
    assert (
        "https://conda.anaconda.org/conda-forge/noarch/python_abi-3.13-7_cp313.conda"
        in data
    )
    assert "0595134584589064f56e67d3de1d8fcbb673a972946bce25fb593fb092fdcd97" in data
    assert "@EXPLICIT" in data
