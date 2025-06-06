from __future__ import annotations

import sys
from contextlib import nullcontext

from conda.base.constants import UNKNOWN_CHANNEL
from conda.base.context import context
from conda.common import url as common_url
from conda.core.prefix_data import PrefixData
from conda.history import History

from .. import __version__


def export_to_explicit(prefix: str, lockfile_path: str | None) -> None:
    specs = History(prefix).get_requested_specs_map().values()
    with open(lockfile_path, "w") if lockfile_path else nullcontext(sys.stdout) as fh:
        # an opinionated and simplified version of conda.cli.main_list::print_explicit
        fh.write("# This file may be used to create an environment using:\n")
        fh.write("# $ conda create --name <env> --file <this file>\n")
        fh.write(f"# platform: {context.subdir}\n")
        if specs:
            fh.write(f"# specs: {' '.join(str(spec) for spec in specs)}\n")
        fh.write(f"# created-by: conda-lockfiles {__version__}\n")
        fh.write("@EXPLICIT\n")
        for prefix_record in PrefixData(prefix).iter_records_sorted():
            url = prefix_record.get("url")
            if not url or url.startswith(UNKNOWN_CHANNEL):
                fh.write(f"# no URL for: {prefix_record['fn']}")
                continue
            url = common_url.remove_auth(common_url.split_anaconda_token(url)[0])
            sha256 = prefix_record.get("sha256", "")
            fh.write(f"{url}#{sha256}\n")
