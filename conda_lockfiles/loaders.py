from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from conda.base.constants import KNOWN_SUBDIRS
from conda.base.context import context
from conda.models.records import PackageRecord
from ruamel.yaml import YAML

from .utils import build_number_from_build_string

if TYPE_CHECKING:
    from typing import Any
    from collections.abc import Iterable

yaml = YAML(typ="safe")


class BaseLoader:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.data = self._load(path)

    @classmethod
    def supports(cls, path: str | Path) -> bool:
        raise NotImplementedError

    def to_conda_and_pypi(
        self,
        environment: str | None = None,
        platform: str = context.subdir,
    ) -> tuple[Iterable[PackageRecord], Iterable[str]]:
        raise NotImplementedError


class PixiLoader(BaseLoader):
    @classmethod
    def supports(cls, path: str | Path) -> bool:
        path = Path(path)
        if path.name != "pixi.lock":
            return False
        data = cls._load(path)
        if data["version"] != 6:
            return False
        return True

    @staticmethod
    def _load(path) -> dict[str, Any]:
        with open(path) as f:
            return yaml.load(f)

    def to_conda_and_pypi(
        self,
        environment: str = "default",
        platform: str = context.subdir,
    ) -> tuple[Iterable[PackageRecord], Iterable[str]]:
        env = self.data["environments"].get(environment)
        if not env:
            raise ValueError(
                f"Environment {environment} not found. "
                f"Available environment names: {sorted(self.data['environments'])}."
            )
        packages = env["packages"].get(platform)
        if not packages:
            raise ValueError(
                f"Environment {environment} does not list packages for platform {platform}. "
                f"Available platforms: {sorted(env['packages'])}."
            )

        conda, pypi = [], []
        for package in packages:
            for package_type, url in package.items():
                if package_type == "conda":
                    conda.append(self._package_record_from_conda_url(url))
                elif package_type == "pypi":
                    pypi.append(url)

        return conda, pypi

    def _package_record_from_conda_url(self, url: str) -> PackageRecord:
        channel, subdir, filename = url.rsplit("/", 2)
        assert subdir in KNOWN_SUBDIRS, f"Unknown subdir '{subdir}' in package {url}."
        if filename.endswith(".tar.bz2"):
            basename = filename[: -len(".tar.bz2")]
            ext = ".tar.bz2"
        elif filename.endswith(".conda"):
            basename = filename[: -len("conda")]
            ext = ".conda"
        else:
            basename, ext = os.path.splitext(filename)
        assert ext.lower() in (
            ".conda",
            ".tar.bz2",
        ), f"Unknown extension '{ext}' in package {url}."
        name, version, build = basename.rsplit("-", 2)
        build_number = build_number_from_build_string(build)
        record_fields = {
            "name": name,
            "version": version,
            "build": build,
            "build_number": build_number,
            "subdir": subdir,
            "channel": channel,
            "fn": filename,
        }
        for record in self.data["packages"]:
            if record.get("conda", "") == url:
                record_fields.update(record)
                record_fields["url"] = record_fields.pop("conda", None)
                break
        return PackageRecord(**record_fields)


LOADERS = (PixiLoader,)
