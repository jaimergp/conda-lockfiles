from __future__ import annotations

from typing import TYPE_CHECKING

from ruamel.yaml import YAML

from conda_lockfiles.dumpers import rattler_lock

from .. import SINGLE_PACKAGE_ENV

if TYPE_CHECKING:
    from pathlib import Path


def test_export_to_rattler_lock_v6(tmp_path: Path) -> None:
    package_url = (
        "https://conda.anaconda.org/conda-forge/noarch/python_abi-3.13-7_cp313.conda"
    )

    lockfile_path = tmp_path / "pixi.lock"
    rattler_lock.export_to_rattler_lock_v6(str(SINGLE_PACKAGE_ENV), str(lockfile_path))
    assert lockfile_path.exists()

    data = YAML().load(lockfile_path)

    assert data["version"] == 6

    # environments object
    assert "environments" in data
    assert "default" in data["environments"]
    default_env = data["environments"]["default"]
    assert "channels" in default_env
    assert "conda-forge" in default_env["channels"][0]["url"]
    assert "packages" in default_env
    subdirs_packages = tuple(default_env["packages"].values())
    assert len(subdirs_packages) == 1
    subdir_packages = subdirs_packages[0]
    assert len(subdir_packages) == 1
    assert subdir_packages[0]["conda"] == package_url

    # packages object
    assert "packages" in data
    packages = data["packages"]
    assert len(packages) == 1
    package = packages[0]
    assert package["conda"] == package_url
    assert (
        package["sha256"]
        == "0595134584589064f56e67d3de1d8fcbb673a972946bce25fb593fb092fdcd97"
    )
    assert package["md5"] == "e84b44e6300f1703cb25d29120c5b1d8"
    assert package["license"] == "BSD-3-Clause"
    assert package["size"] == 6988
    assert "python 3.13.* *_cp313" in package["constrains"]
