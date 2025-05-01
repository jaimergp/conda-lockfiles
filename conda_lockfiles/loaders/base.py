from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from conda.base.context import context
from conda.models.records import PackageRecord

if TYPE_CHECKING:
    from typing import Any
    from collections.abc import Iterable

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
