#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
"""Environment/version snapshot types shared by the version subsystem and crash reporting.

``VersionInfo`` is produced by :mod:`cmk.ccc.version` (the ``general_version_infos*``
functions) and consumed by the crash-reporting library to build a ``CrashInfo``. It
lives here, in the foundational ``cmk.ccc`` layer alongside its producer, so that higher
layers (``cmk.crash``) depend downward on it rather than the reverse.
"""

from collections.abc import Sequence
from typing import TypedDict


class VersionInfoBase(TypedDict):
    """Environment fields shared between ``VersionInfo`` and the crash-reporting ``CrashInfo``.

    ``time`` is intentionally absent from this base class: ``VersionInfo`` carries the raw
    construction-time timestamp as ``time: float`` (used when *constructing* a new crash
    report), whereas the crash-reporting models keep their own time representation
    (``CrashInfo.time: float`` for a single occurrence, ``AggregatedCrashInfo.occurrences``
    for the persisted, deduplicated record).
    """

    core: str
    python_version: str
    edition: str
    python_paths: Sequence[str]
    version: str
    os: str


class VersionInfo(VersionInfoBase):
    """Carries the raw construction-time timestamp as a float."""

    time: float
