from __future__ import annotations

import os
import sys
from collections.abc import Mapping
from subprocess import run
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING

from conda.base.context import context
from conda.common.compat import on_win
from conda.core.link import PrefixSetup, UnlinkLinkTransaction
from conda.core.package_cache_data import PackageCacheData, ProgressiveFetchExtract
from conda.core.prefix_data import PrefixData
from conda.exceptions import CondaExitZero, DryRunExit
from conda.models.prefix_graph import PrefixGraph
from conda.models.records import PackageRecord

from .exceptions import LockfileFormatNotSupported
from .loaders import LOADERS

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path
    from subprocess import CompletedProcess
    from typing import Any

    from conda.common.path import PathType
    from conda.models.match_spec import MatchSpec


def create_environment_from_lockfile(
    lockfile: PathType | Path,
    prefix: PathType | Path,
    environment: str | None = None,
    platform: str = context.subdir,
    dry_run: bool = False,
    download_only: bool = False,
    verbose: bool = False,
) -> None:
    for Loader in LOADERS:
        if Loader.supports(lockfile):
            break
    else:
        raise LockfileFormatNotSupported(lockfile)

    loader = Loader(lockfile)
    conda_specs, pypi_records = loader.to_conda_and_pypi(environment, platform)

    if dry_run:
        raise DryRunExit()

    if conda_specs:
        if verbose:
            print("Installing Conda packages:")
        conda_records = lookup_conda_records(conda_specs)

        if download_only:
            raise CondaExitZero(
                "Package caches prepared. Installation cancelled with --download-only."
            )

        install_conda_records(conda_records, prefix, verbose)

    if pypi_records:
        if verbose:
            print("Installing PyPI packages:")
        install_pypi_records(pypi_records, prefix)


def install_pypi_records(
    urls: Iterable[str],
    prefix: PathType | Path,
) -> CompletedProcess:
    with NamedTemporaryFile("w", delete=False) as f:
        f.write("\n".join(urls))

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


def lookup_conda_records(
    specs: Iterable[MatchSpec] | Mapping[MatchSpec, dict[str, Any]],
) -> tuple[PackageRecord, ...]:
    # normalize specs to a mapping
    if not isinstance(specs, Mapping):
        specs = dict.fromkeys(specs)
    specs = dict(specs)

    # populate package cache
    pfe = ProgressiveFetchExtract(specs.keys())
    pfe.execute()

    # lookup records in package cache
    records: list[PackageRecord] = []
    for match_spec, overrides in specs.items():
        cache_record = next(PackageCacheData.query_all(match_spec), None)
        if cache_record is None:
            raise AssertionError(f"Missing package cache record for: {match_spec}")
        records.append(PackageRecord.from_objects(cache_record, **(overrides or {})))
    return tuple(records)


def install_conda_records(
    records: Iterable[PackageRecord], prefix: PathType | Path, verbose: bool = False
) -> None:
    # determine which packages need to be linked and unlinked
    unlink_precs: list[PackageRecord] = []
    link_precs: list[PackageRecord] = []
    prefix_data = PrefixData(prefix)
    for record in PrefixGraph(records).graph:
        installed_record = prefix_data.get(record.name, None)
        if installed_record:
            # record is already installed, do not re-linking it
            if installed_record != record:
                unlink_precs.append(installed_record)
                link_precs.append(record)
        else:
            link_precs.append(record)

    # create and execute transaction
    stp = PrefixSetup(
        target_prefix=str(prefix),
        unlink_precs=tuple(unlink_precs),
        link_precs=tuple(link_precs),
        remove_specs=(),
        update_specs=(),
        neutered_specs=(),
    )
    txn = UnlinkLinkTransaction(stp)
    if verbose:
        txn.print_transaction_summary()
    txn.execute()
