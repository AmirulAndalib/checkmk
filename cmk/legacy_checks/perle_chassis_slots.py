#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
)
from cmk.plugins.perle.agent_based.perle_chassis_slots import Section
from cmk.plugins.perle.lib import perle_check_alarms

_MAP_DIAG_STATES = {
    "0": (State.OK, "passed"),
    "1": (State.CRIT, "media converter module's PHY is not functional"),
    "2": (State.WARN, "firmware download required"),
}


def discover_perle_chassis_slots(section: Section) -> DiscoveryResult:
    for (
        index,
        _name,
        _modelname,
        _serial,
        _bootloader,
        _fw,
        _alarms,
        _diagstate,
        ty,
        _descr,
    ) in section:
        if ty != "0":
            yield Service(item=index)


def check_perle_chassis_slots(item: str, section: Section) -> CheckResult:
    for (
        index,
        name,
        _modelname,
        _serial,
        _bootloader,
        _fw,
        alarms_str,
        diagstate,
        _ty,
        _descr,
    ) in section:
        if item == index:
            state, state_readable = _MAP_DIAG_STATES[diagstate]
            yield Result(state=state, summary=f"[{name}] Diagnostic result: {state_readable}")
            yield perle_check_alarms(alarms_str)


check_plugin_perle_chassis_slots = CheckPlugin(
    name="perle_chassis_slots",
    service_name="Chassis status slot %s",
    discovery_function=discover_perle_chassis_slots,
    check_function=check_perle_chassis_slots,
)
