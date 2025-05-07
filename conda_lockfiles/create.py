from __future__ import annotations

import os
import sys
from subprocess import run
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING

from conda.base.context import context
from conda.common.compat import on_win
from conda.misc import explicit
from conda.models.prefix_graph import PrefixGraph

from .exceptions import LockfileFormatNotSupported
from .loaders import LOADERS

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path
    from subprocess import CompletedProcess

    from conda.common.path import PathType
    from conda.models.records import PackageRecord


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


def install_pypi_records(pypi_records: Iterable[str], prefix: str) -> CompletedProcess:
    if not pypi_records:
        return
    with NamedTemporaryFile("w", delete=False) as f:
        f.write("\n".join(pypi_records))

    if on_win:
        python_exe = os.path.join(prefix, "python.exe")
    else:
        python_exe = os.path.join(prefix, "bin", "python")
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--prefix",
        prefix,
        "-r",
        f.name,
        "--no-deps",
        "--python",
        python_exe,
    ]
    try:
        return run(command, check=True)
    finally:
        os.unlink(f.name)


def as_explicit(
    records: Iterable[PackageRecord],
    **comments,
) -> Iterable[str]:
    for key, value in comments.items():
        yield f"# {key}: {value}"
    yield "@EXPLICIT"
    for record in dict.fromkeys(PrefixGraph(records).graph):
        yield f"{record.url}#{record.sha256}"
