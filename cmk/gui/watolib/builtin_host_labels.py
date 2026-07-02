#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
"""The common config-generation plugin for the builtin host labels.

Writes the ``cmk/site`` builtin host label into the per-site builtin host labels file
via the ``pre-activate-changes`` hook.

Why this hook (rather than distributing the file, or a config domain):
- The hook fires immediately before a ``restart``/``reload`` automation executes, i.e.
  strictly before the core config is rebuilt from it, on whichever site runs the
  restart. Central, remote and standalone sites all restart their core locally during
  their own activation.
- The file is never synced from the central site (like the discovered host labels
  file); the central site is excluded from snapshot creation, so a central-only or
  distributed writer could not cover it anyway.

The managed-services edition registers a sibling hook that adds ``cmk/customer`` the
same way; keeping one key per hook (merged via ``update_builtin_host_labels``) is what
lets base stay edition-agnostic while the MT label is contributed only when that
edition is shipped. Site creation, version update and site rename are covered by the
sample-config, update-config and post-rename plugins respectively; this hook merely
refreshes the file before every core config generation.
"""

import cmk.utils.paths
from cmk.ccc.site import omd_site
from cmk.ruleset_matcher.labels import BuiltinLabelsKey, update_builtin_host_labels


def update_builtin_host_labels_file(_unused_collect_all_hosts: object) -> None:
    update_builtin_host_labels(
        cmk.utils.paths.builtin_host_labels_file, {BuiltinLabelsKey.SITE: str(omd_site())}
    )
