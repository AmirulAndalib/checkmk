# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

"""Filesystem locations of the persistent overlay data for one site.

Kept free of further dependencies so that modules which only need the
locations (e.g. site resolution, orphan cleanup) don't have to import the
mount machinery in :mod:`cmk.dev_deploy.site.overlay`.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Self

# Persistent storage for overlay upper/work directories.
# /var/tmp survives reboots (unlike /tmp which may be tmpfs).
OVERLAY_BASE = Path("/var") / "tmp" / "cmk-dev-deploy"


@dataclass(frozen=True, kw_only=True)
class OverlayPaths:
    """All overlay filesystem locations for one site."""

    site_overlay: Path
    upper: Path
    work: Path

    @classmethod
    def for_site(cls, site_root: Path, base_dir: Path = OVERLAY_BASE) -> Self:
        site_overlay = base_dir / site_root.name
        return cls(
            site_overlay=site_overlay,
            upper=site_overlay / "upper",
            work=site_overlay / "work",
        )

    @property
    def version_marker(self) -> Path:
        """File recording which OMD version was materialized."""
        return self.site_overlay / "materialized_version"

    @property
    def site_inode_marker(self) -> Path:
        """File recording the bare site-root inode for reinstall detection."""
        return self.site_overlay / "site_inode"

    @property
    def markers_dir(self) -> Path:
        """Per-directory materialization completion markers."""
        return self.site_overlay / "markers"
