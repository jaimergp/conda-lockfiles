from __future__ import annotations

import os
import sys
from subprocess import run
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING

from conda.base.context import context
from conda.common.compat import on_win
from conda.core.link import PrefixSetup, UnlinkLinkTransaction
from conda.core.prefix_data import PrefixData
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

    install_conda_records(conda, prefix)
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


def install_conda_records(records: Iterable[PackageRecord], prefix: str) -> None:
    unlink_precs: list[PackageRecord] = []
    link_precs: list[PackageRecord] = []
    prefix_data = PrefixData(prefix)
    for record in PrefixGraph(records).graph:
        installed_record = prefix_data.get(record.name, None)
        if installed_record:
            # If the record is already installed, do not re-linking it
            if installed_record != record:
                unlink_precs.append(installed_record)
                link_precs.append(record)
        else:
            link_precs.append(record)
    stp = PrefixSetup(
        target_prefix=prefix,
        unlink_precs=tuple(unlink_precs),
        link_precs=tuple(link_precs),
        remove_specs=(),
        update_specs=(),
        neutered_specs=(),
    )
    txn = UnlinkLinkTransaction(stp)
    if not context.json and not context.quiet:
        txn.print_transaction_summary()
    txn.execute()
