""" """

from __future__ import annotations
from typing import TYPE_CHECKING

from conda.base.context import context
from conda.misc import explicit

from .exceptions import LockfileFormatNotSupported
from .loaders import LOADERS
from .utils import as_explicit, install_pypi_records

if TYPE_CHECKING:
    from conda.common.path import PathType
    from pathlib import Path


def create_environment_from_lockfile(
    lockfile: PathType | Path,
    prefix: PathType | Path,
    environment: str | None = None,
    platform: str = context.subdir,
    verbose: bool = True,
) -> None:
    for Loader in LOADERS:
        if Loader.supports(lockfile):
            break
    else:
        raise LockfileFormatNotSupported(lockfile)

    loader = Loader(lockfile)
    conda, pypi = loader.to_conda_and_pypi(environment=environment, platform=platform)

    explicit(as_explicit(conda), prefix)
    if pypi:
        if verbose:
            print("Installing PyPI packages:")
        install_pypi_records(pypi, prefix)
