from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from conda.base.context import context

if TYPE_CHECKING:
    from collections.abc import Iterable

    from conda.models.records import PackageRecord


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
