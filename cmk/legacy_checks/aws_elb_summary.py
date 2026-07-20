#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# mypy: disable-error-code="type-arg"

from collections.abc import Iterable, Sequence

from cmk.agent_based.legacy.v0_unstable import LegacyCheckDefinition
from cmk.agent_based.v2 import StringTable
from cmk.legacy_includes.aws import check_aws_elb_summary_generic, ELBSummaryLoadBalancer
from cmk.plugins.aws.lib import parse_aws

check_info = {}


def parse_aws_elb_summary(string_table: StringTable) -> Sequence[ELBSummaryLoadBalancer]:
    return [
        ELBSummaryLoadBalancer(
            load_balancer_name=load_balancer["LoadBalancerName"],
            # elb (v1) provides availability zones as a list of zone strings.
            availability_zones=load_balancer["AvailabilityZones"],
        )
        for load_balancer in parse_aws(string_table)
    ]


def discover_aws_elb_summary(
    section: Sequence[ELBSummaryLoadBalancer],
) -> Iterable[tuple[None, dict]]:
    if section:
        yield None, {}


check_info["aws_elb_summary"] = LegacyCheckDefinition(
    name="aws_elb_summary",
    parse_function=parse_aws_elb_summary,
    service_name="AWS/ELB Summary",
    discovery_function=discover_aws_elb_summary,
    check_function=check_aws_elb_summary_generic,
)
