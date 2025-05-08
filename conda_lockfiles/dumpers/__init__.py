from __future__ import annotations

from .conda_lock_v1 import export_to_conda_lock_v1

__all__ = ["export_to_conda_lock_v1", "LOCKFILE_FORMATS"]

LOCKFILE_FORMATS: dict[str, callable] = {
    "conda-lock-v1": export_to_conda_lock_v1,
}
