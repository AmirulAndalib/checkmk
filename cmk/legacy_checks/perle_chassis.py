#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_value_store,
    Result,
    Service,
    State,
)
from cmk.plugins.lib.temperature import check_temperature, TempParamType
from cmk.plugins.perle.agent_based.perle_chassis import _Section
from cmk.plugins.perle.lib import perle_check_alarms

_MAP_DIAG_STATES = {
    "0": (State.OK, "passed"),
    "1": (State.WARN, "firmware download required"),
    "2": (State.CRIT, "temperature sensor not functional"),
}


def discover_perle_chassis(section: _Section) -> DiscoveryResult:
    yield Service()


def check_perle_chassis(section: _Section) -> CheckResult:
    state, state_readable = _MAP_DIAG_STATES[section.diagnosis_state]
    yield Result(state=state, summary=f"Diagnostic result: {state_readable}")
    yield perle_check_alarms(section.alarms)


check_plugin_perle_chassis = CheckPlugin(
    name="perle_chassis",
    service_name="Chassis status",
    discovery_function=discover_perle_chassis,
    check_function=check_perle_chassis,
)


def discover_perle_chassis_temp(section: _Section) -> DiscoveryResult:
    yield Service(item="chassis")


def check_perle_chassis_temp(item: str, params: TempParamType, section: _Section) -> CheckResult:
    yield from check_temperature(
        reading=section.temp,
        params=params,
        unique_name="perle_chassis_temp",
        value_store=get_value_store(),
    )


check_plugin_perle_chassis_temp = CheckPlugin(
    name="perle_chassis_temp",
    sections=["perle_chassis"],
    service_name="Temperature %s",
    discovery_function=discover_perle_chassis_temp,
    check_function=check_perle_chassis_temp,
    check_ruleset_name="temperature",
    check_default_parameters={},
)
