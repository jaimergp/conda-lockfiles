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

    from .base import CondaSpecs_v1, PypiRecords

yaml: Final = YAML(typ="safe")

PIXI_LOCK_FILE: Final = "pixi.lock"


class PixiLoader(BaseLoader):
    @classmethod
    def supports(cls, path: PathType) -> bool:
        path = Path(path)
        if path.name != PIXI_LOCK_FILE or not path.exists():
            return False
        data = cls._load(path)
        if data["version"] != 6:
            return False
        return True

    @staticmethod
    def _load(path: PathType) -> dict[str, Any]:
        with open(path) as f:
            return yaml.load(f)

    def to_conda_and_pypi(
        self,
        environment: str | None = "default",
        platform: str = context.subdir,
    ) -> tuple[CondaSpecs_v1, PypiRecords]:
        env = self.data.get("environments", {}).get(environment)
        if not env:
            raise ValueError(
                f"Environment {environment} not found. "
                f"Available environment names: {sorted(self.data['environments'])}."
            )

        platforms = env.get("packages", {})
        if platform not in platforms:
            raise ValueError(
                f"Lockfile environment {environment} does not list packages for "
                f"platform {platform}. "
                f"Available platforms: {', '.join(sorted(platforms))}."
            )
        packages = platforms[platform]

        metadatas = {}
        for package in self.data.get("packages", []):
            if "conda" in package:
                metadatas[("conda", package["conda"])] = package
            elif "pypi" in package:
                metadatas[("pypi", package["pypi"])] = package
            else:
                raise ValueError(f"Unknown package type: {', '.join(sorted(package))}")

        conda = []
        pypi = []
        for package in packages:
            for package_type, url in package.items():
                if not (metadata := metadatas.get((package_type, url))):
                    raise ValueError(f"Unknown package: {url}")

                if package_type == "conda":
                    spec = self._parse_package(url, metadata)
                    conda.append(spec)
                elif package_type == "pypi":
                    pypi.append(url)
                else:
                    raise ValueError(f"Unknown package type: {package_type}")

        return tuple(conda), tuple(pypi)

    @staticmethod
    def _parse_package(url: str, package: dict[str, Any]) -> MatchSpec:
        hashes = subdict(package.get("hash", {}), ["md5", "sha256"])
        return MatchSpec(url, **hashes)
