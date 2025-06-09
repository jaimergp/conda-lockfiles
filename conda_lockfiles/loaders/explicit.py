from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

from conda.base.context import context
from conda.common.path import expand
from conda.common.url import is_url, join_url, path_to_url
from conda.exceptions import ParseError

from .base import BaseLoader
from .records_from_urls import records_from_conda_urls

if TYPE_CHECKING:
    from typing import Any, Final

    from conda.common.path import PathType
    from conda.models.records import PackageRecord

    from .records_from_urls import CondaPackageMetadata, CondaPackageURL


URL_PAT = re.compile(
    r"(?:(?P<url_p>.+)(?:[/\\]))?"
    r"(?P<fn>[^/\\#]+(?:\.tar\.bz2|\.conda))"
    r"(?:#("
    r"(?P<md5>[0-9a-f]{32})"
    r"|((sha256:)?(?P<sha256>[0-9a-f]{64}))"
    r"))?$"
)

EXPLICIT_KEY: Final = "@EXPLICIT"


class ExplicitLoader(BaseLoader):
    @classmethod
    def supports(cls, path: PathType) -> bool:
        path = Path(path)
        if not path.exists():
            return False
        data = cls._load(path)
        if EXPLICIT_KEY not in data:
            return False
        return True

    @staticmethod
    def _load(path: PathType) -> dict[str, Any]:
        return Path(path).read_text()

    def to_conda_and_pypi(
        self,
        environment: str = "default",
        platform: str = context.subdir,
    ) -> tuple[tuple[PackageRecord, ...], tuple[str, ...]]:
        conda_metadata_by_url = {}
        for line in self.data.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line == EXPLICIT_KEY:
                continue
            url, metadata = self._parse_line(line)
            conda_metadata_by_url[url] = metadata
        conda = records_from_conda_urls(conda_metadata_by_url)
        return conda, tuple()

    @staticmethod
    def _parse_line(line: str) -> tuple[CondaPackageURL, CondaPackageMetadata]:
        # adapted from conda.misc::_match_specs_from_explicit
        if not is_url(line):
            line = path_to_url(expand(line))
        # parse URL
        match = URL_PAT.match(line)
        if match is None:
            raise ParseError(f"Could not parse explicit URL: {line}")
        # url_p is everything but the tarball_basename and the checksum
        url_p, fn = match.group("url_p"), match.group("fn")
        url = join_url(url_p, fn)
        metadata = {}
        if md5 := match.group("md5"):
            metadata["md5"] = md5
        if sha256 := match.group("sha256"):
            metadata["sha256"] = sha256
        return url, metadata
