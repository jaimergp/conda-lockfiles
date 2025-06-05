from __future__ import annotations

from .conda_lock_v1 import export_to_conda_lock_v1
from .pixi import export_to_pixi_v6

__all__ = [
    "export_to_conda_lock_v1",
    "export_to_pixi_v6",
    "LOCKFILE_FORMATS",
]

LOCKFILE_FORMATS: dict[str, callable] = {
    "conda-lock-v1": export_to_conda_lock_v1,
    "pixi-v6": export_to_pixi_v6,
}
