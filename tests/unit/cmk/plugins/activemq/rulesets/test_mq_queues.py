#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping

import pytest

from cmk.plugins.activemq.rulesets.mq_queues import _migrate


@pytest.mark.parametrize(
    "inp, expected",
    [
        pytest.param(
            {"consumerCount": (10, 20), "size": (5, 6)},
            {"consumer_count_levels_upper": (10, 20), "size": (5, 6)},
            id="legacy consumerCount -> upper",
        ),
        pytest.param(
            {"consumerCount": (10, 5), "size": (5, 6)},
            {"consumer_count_levels_lower": (10, 5), "size": (5, 6)},
            id="legacy consumerCount -> lower",
        ),
        pytest.param(
            {"consumerCount": (10, 10)},
            {"consumer_count_levels_lower": (10, 10)},
            id="equal values -> lower",
        ),
        pytest.param(
            {"size": (5, 6)},
            {"size": (5, 6)},
            id="no consumerCount -> passthrough",
        ),
        pytest.param(
            {
                "size": ("fixed", (0, 0)),
                "consumer_count_levels_upper": ("fixed", (10, 20)),
            },
            {
                "size": ("fixed", (0, 0)),
                "consumer_count_levels_upper": ("fixed", (10, 20)),
            },
            id="already migrated -> passthrough",
        ),
    ],
)
def test_migrate(inp: Mapping[str, object], expected: Mapping[str, object]) -> None:
    assert _migrate(inp) == expected
