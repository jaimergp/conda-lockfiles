from __future__ import annotations

from typing import TYPE_CHECKING

from .dumpers import LOCKFILE_FORMATS
from .exceptions import ExportLockfileFormatNotSupported


if TYPE_CHECKING:
    from typing import Any, Optional


def export_environment_to_lockfile(
    lockfile_format: str, prefix: str, lockfile_path: Optional[str]
) -> None:
    if lockfile_format not in LOCKFILE_FORMATS:
        raise ExportLockfileFormatNotSupported(lockfile_format)
    return LOCKFILE_FORMATS[lockfile_format](prefix, lockfile_path)
