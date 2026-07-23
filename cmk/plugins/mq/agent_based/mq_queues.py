#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# Example output from agent:
# [[SINGLE_ITEM_EXPORT_int_jens]]
# 0 0 0 0
# [[SPRINGAPP-COMMAND-INBOX-DEV]]
# 0 0 15 15
# [[SINGLE_ITEM_EXPORT_INT_jens]]
# 0 0 0 0
# [[DEBITOR_LOCATION]]
# 0 1 84 84
# [[EDATA_SERIALNUMBERQUERY_INBOX]]
# 0 0 0 0

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TypedDict

from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Service,
    StringTable,
)
from cmk.rulesets.v1.form_specs import SimpleLevelsConfigModel


@dataclass(frozen=True)
class Queue:
    size: int
    consumer_count: int
    enqueue_count: int
    dequeue_count: int


Section = Mapping[str, Queue]


class Params(TypedDict):
    size: SimpleLevelsConfigModel[int]
    consumer_count_levels_upper: SimpleLevelsConfigModel[int]
    consumer_count_levels_lower: SimpleLevelsConfigModel[int]


def parse_mq_queues(string_table: StringTable) -> Section:
    section: dict[str, Queue] = {}
    item: str | None = None
    for line in string_table:
        if line[0].startswith("[["):
            item = line[0][2:-2]
        elif item is not None:
            size, consumer_count, enqueue_count, dequeue_count = (int(x) for x in line)
            section[item] = Queue(size, consumer_count, enqueue_count, dequeue_count)
    return section


agent_section_mq_queues = AgentSection(
    name="mq_queues",
    parse_function=parse_mq_queues,
)


def discover_mq_queues(section: Section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)


def check_mq_queues(item: str, params: Params, section: Section) -> CheckResult:
    if (queue := section.get(item)) is None:
        return
    yield from check_levels(
        queue.consumer_count,
        levels_upper=params["consumer_count_levels_upper"],
        levels_lower=params["consumer_count_levels_lower"],
        render_func=str,
        label="Consuming connections",
        notice_only=True,
    )
    yield from check_levels(
        queue.size,
        levels_upper=params["size"],
        metric_name="queue",
        render_func=str,
        label="Queue size",
    )
    yield from check_levels(
        queue.enqueue_count,
        metric_name="enque",
        render_func=str,
        label="Enqueue count",
    )
    yield from check_levels(
        queue.dequeue_count,
        metric_name="deque",
        render_func=str,
        label="Dequeue count",
    )


check_plugin_mq_queues = CheckPlugin(
    name="mq_queues",
    service_name="Queue %s",
    discovery_function=discover_mq_queues,
    check_function=check_mq_queues,
    check_ruleset_name="mq_queues",
    check_default_parameters=Params(
        size=("no_levels", None),
        consumer_count_levels_upper=("no_levels", None),
        consumer_count_levels_lower=("no_levels", None),
    ),
)
