#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Sequence

import pytest

from cmk.agent_based.v2 import Metric, Result, Service, State, StringTable
from cmk.plugins.activemq.agent_based.mq_queues import (
    check_mq_queues,
    discover_mq_queues,
    Params,
    parse_mq_queues,
    Queue,
    Section,
)

_STRING_TABLE: StringTable = [
    ["[[Queue_App1_App2]]"],
    ["1", "2", "3", "4"],
    ["[[M2M_DC_MGMT]]"],
    ["0", "12", "9193", "9193"],
]


def test_parse_mq_queues() -> None:
    assert parse_mq_queues(_STRING_TABLE) == {
        "Queue_App1_App2": Queue(size=1, consumer_count=2, enqueue_count=3, dequeue_count=4),
        "M2M_DC_MGMT": Queue(size=0, consumer_count=12, enqueue_count=9193, dequeue_count=9193),
    }


def test_discover_mq_queues() -> None:
    assert list(discover_mq_queues(parse_mq_queues(_STRING_TABLE))) == [
        Service(item="Queue_App1_App2"),
        Service(item="M2M_DC_MGMT"),
    ]


_DEFAULT_PARAMS = Params(
    size=("no_levels", None),
    consumer_count_levels_upper=("no_levels", None),
    consumer_count_levels_lower=("no_levels", None),
)


@pytest.mark.parametrize(
    "item, params, section, expected_results",
    [
        pytest.param(
            "Queue_App1_App2",
            _DEFAULT_PARAMS,
            {"Queue_App1_App2": Queue(1, 2, 3, 4)},
            [
                Result(state=State.OK, notice="Consuming connections: 2"),
                Result(state=State.OK, summary="Queue size: 1"),
                Metric("queue", 1.0),
                Result(state=State.OK, summary="Enqueue count: 3"),
                Metric("enque", 3.0),
                Result(state=State.OK, summary="Dequeue count: 4"),
                Metric("deque", 4.0),
            ],
            id="no levels, consumer count only in details",
        ),
        pytest.param(
            "M2M_DC_MGMT",
            Params(
                size=("fixed", (6, 10)),
                consumer_count_levels_upper=("fixed", (5, 9)),
                consumer_count_levels_lower=("fixed", (3, 1)),
            ),
            {"M2M_DC_MGMT": Queue(0, 12, 9193, 9193)},
            [
                Result(
                    state=State.CRIT,
                    notice="Consuming connections: 12 (warn/crit at 5/9)",
                ),
                Result(state=State.OK, summary="Queue size: 0"),
                Metric("queue", 0.0, levels=(6.0, 10.0)),
                Result(state=State.OK, summary="Enqueue count: 9193"),
                Metric("enque", 9193.0),
                Result(state=State.OK, summary="Dequeue count: 9193"),
                Metric("deque", 9193.0),
            ],
            id="upper consumer count breached",
        ),
        pytest.param(
            "M2M_DATA_RESPONSE",
            Params(
                size=("fixed", (6, 10)),
                consumer_count_levels_upper=("fixed", (5, 9)),
                consumer_count_levels_lower=("fixed", (3, 1)),
            ),
            {"M2M_DATA_RESPONSE": Queue(0, 1, 9193, 9193)},
            [
                Result(
                    state=State.WARN,
                    notice="Consuming connections: 1 (warn/crit below 3/1)",
                ),
                Result(state=State.OK, summary="Queue size: 0"),
                Metric("queue", 0.0, levels=(6.0, 10.0)),
                Result(state=State.OK, summary="Enqueue count: 9193"),
                Metric("enque", 9193.0),
                Result(state=State.OK, summary="Dequeue count: 9193"),
                Metric("deque", 9193.0),
            ],
            id="lower consumer count breached",
        ),
        pytest.param(
            "missing",
            _DEFAULT_PARAMS,
            {"other": Queue(1, 2, 3, 4)},
            [],
            id="unknown item yields nothing",
        ),
    ],
)
def test_check_mq_queues(
    item: str,
    params: Params,
    section: Section,
    expected_results: Sequence[object],
) -> None:
    assert list(check_mq_queues(item, params, section)) == expected_results
