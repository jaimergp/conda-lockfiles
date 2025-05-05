from __future__ import annotations

from .base import BaseLoader
from .pixi import PixiLoader

__all__ = ["BaseLoader", "PixiLoader", "LOADERS"]

LOADERS = (PixiLoader,)
