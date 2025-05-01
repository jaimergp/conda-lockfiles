from __future__ import annotations

import os
import sys
from shutil import which
from subprocess import run, CompletedProcess
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

from conda.common.compat import on_win
from conda.models.records import PackageRecord
from conda.models.prefix_graph import PrefixGraph
from ruamel.yaml import YAML

yaml = YAML(typ="safe")


def install_pypi_records(pypi_records: Iterable[str], prefix: str) -> CompletedProcess:
    if not pypi_records:
        return
    with NamedTemporaryFile("w", delete=False) as f:
        f.write("\n".join(pypi_records))

    if executable := which("uv"):
        command = [executable]
    else:
        command = [sys.executable, "-m"]
    if on_win:
        python_exe = os.path.join(prefix, "python.exe")
    else:
        python_exe = os.path.join(prefix, "bin", "python")
    command += [
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
