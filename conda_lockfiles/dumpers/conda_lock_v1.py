from __future__ import annotations

from typing import TYPE_CHECKING
import datetime
from contextlib import nullcontext
import sys

from conda.base.context import context
from conda.core.prefix_data import PrefixData
from conda.models.match_spec import MatchSpec

from ruamel.yaml import YAML


if TYPE_CHECKING:
    from typing import Any, Optional

    from conda.models.records import PackageRecord


def _record_to_conda_lock_v1_package(
    record: PackageRecord, platform: str
) -> dict[str, Any]:
    dependencies = {}
    for dep in record.depends:
        ms = MatchSpec(dep)
        version = ms.version.spec_str if ms.version is not None else ""
        dependencies[ms.name] = version
    _hash = {}
    if record.md5:
        _hash["md5"] = record.md5
    if record.sha256:
        _hash["sha256"] = record.sha256
    return {
        "name": record.name,
        "version": record.version,
        "manager": "conda",
        "platform": platform,
        "dependencies": dependencies,
        "url": record.url,
        "hash": _hash,
        "category": "main",
        "optional": False,
    }


def export_to_conda_lock_v1(prefix: str, lockfile_path: Optional[str]) -> None:
    prefix_data = PrefixData(prefix)
    packages = [
        _record_to_conda_lock_v1_package(p, context.subdir)
        for p in prefix_data.iter_records()
    ]
    channel_urls = {(p.schannel) for p in prefix_data.iter_records()}
    metadata = {
        "content_hash": {},
        "channels": [{"url": url, "used_env_vars": []} for url in channel_urls],
        "platforms": [context.subdir],
        "sources": [""],
        "time_metadata": {
            "created_at": datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
        },
        "custom_metadata": {
            "created_by": "conda-lockfiles",
        },
    }
    output = {
        "version": 1,
        "metadata": metadata,
        "package": sorted(packages, key=lambda x: x["name"]),
    }
    with open(lockfile_path, "w") if lockfile_path else nullcontext(sys.stdout) as fh:
        YAML().dump(output, stream=fh)
