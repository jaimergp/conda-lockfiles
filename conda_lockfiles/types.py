from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import NotRequired, TypedDict

    from conda.models.match_spec import MatchSpec

    class CondaRecordOverrides(TypedDict):
        depends: NotRequired[list[str]]
        license: NotRequired[str]

    CondaSpecsTuple = tuple[MatchSpec, ...]
    CondaSpecsMapping = Mapping[MatchSpec, CondaRecordOverrides]
    CondaSpecs = CondaSpecsTuple | CondaSpecsMapping
    PypiRecords = tuple[str, ...]
