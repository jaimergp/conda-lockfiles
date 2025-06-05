from __future__ import annotations

from .base import BaseLoader
from .conda_lock_v1 import CondaLockV1Loader
from .explicit import ExplicitLoader
from .pixi import PixiLoader

__all__ = [
    "BaseLoader",
    "CondaLockV1Loader",
    "ExplicitLoader",
    "PixiLoader",
    "LOADERS",
]

LOADERS = (
    CondaLockV1Loader,
    ExplicitLoader,
    PixiLoader,
)
