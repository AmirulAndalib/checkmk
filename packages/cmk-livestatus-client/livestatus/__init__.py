#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
"""MK Livestatus Python API

Deprecated compatibility wrapper, announced in werk #20119.
Use `cmk.livestatus_client` instead.
This module will be removed in a future version of Checkmk (after 3.0).
"""

# TODO: The "bazel lint ..." calls for run_check_format() and run_check_ruff() don't agree on their findings. Why??
from cmk.livestatus_client import *  # noqa: F403,RUF100
