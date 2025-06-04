from __future__ import annotations

import sys
from contextlib import nullcontext
from typing import TYPE_CHECKING

from conda.base.context import context
from conda.core.prefix_data import PrefixData
from conda.models.records import PackageRecord
from ruamel.yaml import YAML

if TYPE_CHECKING:
    from typing import Any

    from conda.models.records import PackageRecord


def _record_to_pixi_v6_package(record: PackageRecord) -> dict[str, Any]:
    package = {
        "conda": record.url,
    }
    # add relevent non-empty fields that rattler_lock includes in v6 lockfiles
    # https://github.com/conda/rattler/blob/rattler_lock-v0.23.5/crates/rattler_lock/src/parse/models/v6/conda_package_data.rs#L46
    fields = [
        # name, version, ... have not been observed in lockfile produced by pixi
        "sha256",
        "md5",
        "depends",
        "constrains",
        "features",
        "track_features",
        "license",
        "license_family",
        "size",
        # conda does not record the repodata timestamp in the environment records
        # do not include this field
        # "timestamp",
        "python_site_packages_path",
    ]
    for field in fields:
        if data := record.get(field, None):
            package[field] = data
    return package


def export_to_pixi_v6(prefix: str, lockfile_path: str | None) -> None:
    prefix_data = PrefixData(prefix)
    channel_urls = {(p.channel) for p in prefix_data.iter_records()}
    channels = [{"url": str(url)} for url in channel_urls]
    env_subdir_pkgs = [{"conda": str(p.url)} for p in prefix_data.iter_records()]
    packages = [_record_to_pixi_v6_package(p) for p in prefix_data.iter_records()]
    environments = {
        "default": {
            "channels": channels,
            "packages": {
                context.subdir: env_subdir_pkgs,
            },
        }
    }
    output = {
        "version": 6,
        "environments": environments,
        "packages": packages,
    }
    with open(lockfile_path, "w") if lockfile_path else nullcontext(sys.stdout) as fh:
        YAML().dump(output, stream=fh)
