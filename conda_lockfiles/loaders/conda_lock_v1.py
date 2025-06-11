from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from conda.base.context import context
from ruamel.yaml import YAML

from ..constants import CONDA_LOCK_FILE
from .base import BaseLoader
from .records_from_urls import records_from_conda_urls

if TYPE_CHECKING:
    from typing import Any

    from conda.common.path import PathType
    from conda.models.records import PackageRecord

    from .records_from_urls import CondaPackageMetadata, CondaPackageURL


yaml = YAML(typ="safe")


class CondaLockV1Loader(BaseLoader):
    @classmethod
    def supports(cls, path: PathType) -> bool:
        path = Path(path)
        if path.name != CONDA_LOCK_FILE or not path.exists():
            return False
        data = cls._load(path)
        if data["version"] != 1:
            return False
        return True

    @staticmethod
    def _load(path: PathType) -> dict[str, Any]:
        with open(path) as f:
            return yaml.load(f)

    def to_conda_and_pypi(
        self,
        environment: str = "default",
        platform: str = context.subdir,
    ) -> tuple[tuple[PackageRecord, ...], tuple[str, ...]]:
        metadata = self.data["metadata"]
        if platform not in metadata["platforms"]:
            raise ValueError(
                f"Lockfile does not list packages for platform {platform}. "
                f"Available platforms: {sorted(metadata['platforms'])}."
            )

        pypi = []
        conda_metadata_by_url: dict[CondaPackageURL, CondaPackageMetadata] = {}
        for package in self.data["package"]:
            if package["platform"] != platform:
                continue
            if package["category"] != "main":
                continue
            if package["optional"]:
                continue
            if package["manager"] == "conda":
                conda_metadata_by_url[package["url"]] = self._package_to_metadata(
                    package
                )
            elif package["manager"] == "pip":
                pypi.append(package["url"])

        conda = records_from_conda_urls(conda_metadata_by_url)
        return conda, pypi

    @staticmethod
    def _package_to_metadata(package: dict[str, Any]) -> CondaPackageMetadata:
        """Return conda record metadata from lockfile package metadata."""
        depends = [
            f"{name} {spec}" for name, spec in package.get("dependencies", {}).items()
        ]
        checksums = {}
        hash_data = package.get("hash", {})
        for checksum_name in ["md5", "sha256"]:
            if checksum_name in hash_data:
                checksums[checksum_name] = hash_data[checksum_name]
        metadata = {
            "name": package["name"],
            "version": package["version"],
            "depends": depends,
            **checksums,
        }
        return metadata
