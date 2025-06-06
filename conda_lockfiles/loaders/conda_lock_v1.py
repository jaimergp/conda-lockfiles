from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from conda.base.context import context
from conda.models.match_spec import MatchSpec
from ruamel.yaml import YAML

from .base import BaseLoader, subdict

if TYPE_CHECKING:
    from typing import Any, Final

    from conda.common.path import PathType

yaml: Final = YAML(typ="safe")

CONDA_LOCK_FILE: Final = "conda-lock.yml"


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
    ) -> tuple[dict[MatchSpec, dict[str, Any]], tuple[str, ...]]:
        platforms = self.data.get("metadata", {}).get("platforms")
        if platform not in platforms:
            raise ValueError(
                f"Lockfile does not list packages for platform {platform}. "
                f"Available platforms: {', '.join(sorted(platforms))}."
            )

        conda: dict[MatchSpec, dict[str, Any]] = {}
        pypi: list[str] = []
        for package in self.data["package"]:
            if package.get("platform") != platform:
                continue
            if package.get("category") != "main":
                continue
            if package.get("optional"):
                continue

            package_type = package.get("manager")
            if package_type == "conda":
                hashes = subdict(package.get("hash", {}), ["md5", "sha256"])
                conda[MatchSpec(package["url"], **hashes)] = {
                    "depends": [
                        f"{name} {spec}"
                        for name, spec in package.get("dependencies", {}).items()
                    ]
                }
            elif package_type == "pip":
                pypi.append(package["url"])
            else:
                raise ValueError(f"Unknown package type: {package_type}")

        return conda, tuple(pypi)
