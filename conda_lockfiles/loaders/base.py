from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from conda.base.context import context

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Any

    from conda.common.path import PathType
    from conda.models.records import PackageRecord


class BaseLoader(ABC):
    def __init__(self, path: PathType):
        self.path = Path(path)
        self.data = self._load(path)

    @classmethod
    @abstractmethod
    def supports(cls, path: PathType) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _load(self, path: PathType) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def to_conda_and_pypi(
        self,
        environment: str | None = None,
        platform: str = context.subdir,
    ) -> tuple[Iterable[PackageRecord], Iterable[str]]:
        raise NotImplementedError


def build_number_from_build_string(build_string: str) -> int:
    "Assume build number is underscore-separated, all-digit substring in build_string"
    return int(
        next(
            (
                part
                for part in build_string.split("_")
                if all(digit.isdigit() for digit in part)
            ),
            0,
        )
    )
