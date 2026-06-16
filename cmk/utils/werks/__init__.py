#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

"""Backwards-compatible re-exports to be removed."""

from cmk.werks.site import (
    COMPILED_WERKS_DIR as COMPILED_WERKS_DIR,
)
from cmk.werks.site import (
    load as load,
)
from cmk.werks.site import (
    load_werk_entries as load_werk_entries,
)
