#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.agent_based.v2 import Result, startswith, State

DETECT_PERLE = startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.1966.20")


def perle_check_alarms(alarms_str: str) -> Result:
    if int(alarms_str) > 0:
        return Result(
            state=State.CRIT,
            summary=f"Alarms: {alarms_str}"
            " (User intervention is needed to resolve the outstanding alarms)",
        )
    return Result(state=State.OK, summary=f"Alarms: {alarms_str}")
