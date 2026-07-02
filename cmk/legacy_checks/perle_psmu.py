#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from collections.abc import Mapping
from typing import Any

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
)
from cmk.plugins.lib.elphase import check_elphase, ElPhase, ReadingWithState
from cmk.plugins.perle.agent_based.perle_psmu import Section


def _discover_perle_psmu(section: Section, what_state: str) -> DiscoveryResult:
    for unit, values in section.items():
        if values[what_state][1] != "not present":
            yield Service(item=unit)


def discover_perle_psmu(section: Section) -> DiscoveryResult:
    yield from _discover_perle_psmu(section, "psustate")


def discover_perle_psmu_fan(section: Section) -> DiscoveryResult:
    yield from _discover_perle_psmu(section, "fanstate")


def check_perle_psmu_powersupplies(
    item: str, params: Mapping[str, Any], section: Section
) -> CheckResult:
    if (data := section.get(item)) is None:
        return
    state, state_readable = data["psustate"]
    yield Result(state=State(state), summary=f"Status: {state_readable}")
    yield from check_elphase(
        params,
        ElPhase(
            voltage=ReadingWithState(value=data["voltage"]) if "voltage" in data else None,
            power=ReadingWithState(value=data["power"]) if "power" in data else None,
        ),
    )


def check_perle_psmu_fans(item: str, section: Section) -> CheckResult:
    if (data := section.get(item)) is None:
        return
    state, state_readable = data["fanstate"]
    yield Result(state=State(state), summary=f"Status: {state_readable}")


check_plugin_perle_psmu = CheckPlugin(
    name="perle_psmu",
    service_name="Power supply %s",
    discovery_function=discover_perle_psmu,
    check_function=check_perle_psmu_powersupplies,
    check_ruleset_name="el_inphase",
    check_default_parameters={},
)


check_plugin_perle_psmu_fan = CheckPlugin(
    name="perle_psmu_fan",
    sections=["perle_psmu"],
    service_name="Fan %s",
    discovery_function=discover_perle_psmu_fan,
    check_function=check_perle_psmu_fans,
)
