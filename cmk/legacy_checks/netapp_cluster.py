#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# netappFiler(1)
# netappClusteredFiler(3)
#                sysStat(2) cf(3)     cfSettings(1)
#                                     cfState(2)
#                                     cfCannotTakeoverCause(3)
#                                     cfPartnerStatus(4)
#                                     cfPartnerName(6)
#                                     cfInterconnectStatus(8)
# SNMPv2-SMI::enterprises.789.1.2.3.1.0 = INTEGER: 2
# SNMPv2-SMI::enterprises.789.1.2.3.2.0 = INTEGER: 2
# SNMPv2-SMI::enterprises.789.1.2.3.3.0 = INTEGER: 1
# SNMPv2-SMI::enterprises.789.1.2.3.4.0 = INTEGER: 2
# SNMPv2-SMI::enterprises.789.1.2.3.6.0 = STRING: "ZMUCFB"
# SNMPv2-SMI::enterprises.789.1.2.3.8.0 = INTEGER: 4


from cmk.agent_based.v2 import (
    all_of,
    CheckPlugin,
    CheckResult,
    contains,
    DiscoveryResult,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    startswith,
    State,
    StringTable,
)


def discover_netapp_cluster(section: StringTable) -> DiscoveryResult:
    if not section:
        return
    (
        cfSettings,
        _cfState,
        _cfCannotTakeoverCause,
        _cfPartnerStatus,
        cfPartnerName,
        _cfInterconnectStatus,
    ) = section[0]
    # only inventorizes clusters that dont have takeover disabled.
    if int(cfSettings) not in [1, 3]:
        # Include the cluster partner name in inventory (value added data)
        yield Service(item=cfPartnerName)


def check_netapp_cluster(item: str, section: StringTable) -> CheckResult:
    (
        cfSettings,
        cfState,
        cfCannotTakeoverCause,
        cfPartnerStatus,
        cfPartnerName,
        cfInterconnectStatus,
    ) = section[0]

    # first handle all critical states.
    # "dead" and "thisNodeDead"
    if cfState == "1" or cfSettings == "5":
        yield Result(state=State.CRIT, summary="Node is declared dead by cluster")
        return
    if cfPartnerStatus in ["1", "3"]:
        yield Result(state=State.CRIT, summary="Partner Status is dead or maybeDown")
        return
    if cfInterconnectStatus == "2":
        yield Result(state=State.CRIT, summary="Cluster Interconnect failure")
        return

    # then handle warnings.
    if cfSettings in ["3", "4"] or cfState == "3":
        yield Result(state=State.WARN, summary="Cluster takeover is disabled")
        return
    if cfInterconnectStatus == "partialFailure":
        yield Result(state=State.WARN, summary="Cluster interconnect partially failed")
        return

    # if the partner name has changed, we'd like to issue a warning
    if cfPartnerName != item:
        yield Result(state=State.WARN, summary=f"Partner Name {cfPartnerName} instead of {item}")
        return

    # OK - Cluster enabled, Cluster can takeover and the partner is OK and the
    # infiniband interconnect is working.
    if all(
        (
            cfSettings == "2",
            cfState == "2",
            cfCannotTakeoverCause == "1",
            cfPartnerStatus == "2",
            cfInterconnectStatus == "4",
        )
    ):
        yield Result(state=State.OK, summary="Cluster Status is OK")
        return

    # if we reach here, we hit an unknown case.
    yield Result(state=State.UNKNOWN, summary="Got unhandled information")
    return


def parse_netapp_cluster(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_netapp_cluster = SimpleSNMPSection(
    name="netapp_cluster",
    detect=all_of(
        contains(".1.3.6.1.2.1.1.1.0", "netapp release"),
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.789"),
    ),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.789.1.2.3",
        oids=["1", "2", "3", "4", "6", "8"],
    ),
    parse_function=parse_netapp_cluster,
)


check_plugin_netapp_cluster = CheckPlugin(
    name="netapp_cluster",
    service_name="metrocluster_w_%s",
    discovery_function=discover_netapp_cluster,
    check_function=check_netapp_cluster,
)
