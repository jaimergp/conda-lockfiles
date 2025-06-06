""" """

from __future__ import annotations

from typing import TYPE_CHECKING

from conda.exceptions import CondaError

if TYPE_CHECKING:
    from pathlib import Path

    from conda.common.path import PathType


class LockfileFormatNotSupported(CondaError):
    def __init__(self, path: PathType | Path):
        message = f"The specified file {path} is not supported."
        super().__init__(message)


class ExportLockfileFormatNotSupported(CondaError):
    def __init__(self, lockfile_format: str):
        message = f"Exporting to lockfile format {lockfile_format} is not supported."
        super().__init__(message)
