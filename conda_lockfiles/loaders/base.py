from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from conda.base.context import context

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping
    from typing import Any, NotRequired, TypedDict, TypeVar

    from conda.common.path import PathType
    from conda.models.match_spec import MatchSpec

    class CondaRecordOverrides(TypedDict):
        depends: NotRequired[list[str]]
        license: NotRequired[str]

    CondaSpecsTuple = tuple[MatchSpec, ...]
    CondaSpecsMapping = Mapping[MatchSpec, CondaRecordOverrides]
    CondaSpecs = CondaSpecsTuple | CondaSpecsMapping
    PypiRecords = tuple[str, ...]

    K = TypeVar("K", bound=str)


class BaseLoader(ABC):
    def __init__(self, path: PathType):
        self.path = Path(path)
        self.data = self._load(path)

    @classmethod
    @abstractmethod
    def supports(cls, path: PathType) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _load(self, path: PathType) -> Any:
        raise NotImplementedError

    @abstractmethod
    def to_conda_and_pypi(
        self,
        environment: str | None = None,
        platform: str = context.subdir,
    ) -> tuple[CondaSpecs, PypiRecords]:
        raise NotImplementedError


def subdict(mapping: Mapping[str, Any], keys: Iterable[K]) -> dict[K, Any]:
    return {key: mapping[key] for key in keys if key in mapping}
