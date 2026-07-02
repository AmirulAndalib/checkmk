#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from collections.abc import Mapping

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
)
from cmk.plugins.perle.lib import DETECT_PERLE

# .1.3.6.1.4.1.1966.21.1.1.1.1.4.5.1.1.2.1.1 1 --> PERLE-MCR-MGT-MIB::mcrMgtSlotIndex.1.1
# .1.3.6.1.4.1.1966.21.1.1.1.1.4.5.1.1.3.1.1 MCR-MGT --> PERLE-MCR-MGT-MIB::mcrMgtModelName.1.1
# .1.3.6.1.4.1.1966.21.1.1.1.1.4.5.3.1.4.1.1 0 --> PERLE-MCR-MGT-MIB::mcrMgtLedALM.1.1

_MAP_ALARM_LED: Mapping[str, tuple[State, str]] = {
    "0": (State.OK, "no alarms"),
    "1": (State.CRIT, "alarms present"),
}
_MAP_POWER_LED: Mapping[str, tuple[State, str]] = {
    "0": (State.CRIT, "off"),
    "1": (State.OK, "on"),
}


def parse_perle_modules_mgt(string_table: StringTable) -> StringTable:
    return string_table


def discover_perle_modules_mgt(section: StringTable) -> DiscoveryResult:
    for index, _name, _descr, _power_led, _alarm_led in section:
        yield Service(item=index)


def check_perle_modules_mgt(item: str, section: StringTable) -> CheckResult:
    for index, _name, _descr, power_led, alarm_led in section:
        if item == index:
            alarm_state, alarm_readable = _MAP_ALARM_LED[alarm_led]
            yield Result(state=alarm_state, summary=f"Alarm LED: {alarm_readable}")
            power_state, power_readable = _MAP_POWER_LED[power_led]
            yield Result(state=power_state, summary=f"Power LED: {power_readable}")


snmp_section_perle_modules_mgt = SimpleSNMPSection(
    name="perle_modules_mgt",
    parse_function=parse_perle_modules_mgt,
    detect=DETECT_PERLE,
    # If you change snmp info please adapt the related inventory plugin,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.1966.21.1.1.1.1.4.5",
        oids=["1.1.2", "1.1.3", "1.1.4", "3.1.3", "3.1.4"],
    ),
)


check_plugin_perle_modules_mgt = CheckPlugin(
    name="perle_modules_mgt",
    service_name="Chassis slot %s MGT",
    discovery_function=discover_perle_modules_mgt,
    check_function=check_perle_modules_mgt,
)
