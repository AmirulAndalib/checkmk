#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from cmk.agent_based.v2 import Metric, Result, Service, State, StringTable
from cmk.plugins.ups.agent_based.ups_in_freq import (
    check_ups_in_freq,
    discover_ups_in_freq,
    parse_ups_in_freq,
)


@pytest.mark.parametrize(
    "string_table, expected",
    [
        ([["1", "500"], ["2", "0"], ["3", ""]], [Service(item="1")]),
        ([], []),
    ],
)
def test_discover_ups_in_freq(string_table: StringTable, expected: list[Service]) -> None:
    assert list(discover_ups_in_freq(parse_ups_in_freq(string_table))) == expected


def test_check_ups_in_freq_ok() -> None:
    section = parse_ups_in_freq([["1", "500"]])
    assert list(check_ups_in_freq("1", {"levels_lower": (45, 40)}, section)) == [
        Result(state=State.OK, summary="50.0 Hz"),
        Metric("in_freq", 50.0, boundaries=(30, 70)),
    ]


def test_check_ups_in_freq_warn() -> None:
    section = parse_ups_in_freq([["1", "430"]])
    assert list(check_ups_in_freq("1", {"levels_lower": (45, 40)}, section)) == [
        Result(state=State.WARN, summary="43.0 Hz (warn/crit below 45 Hz/40 Hz)"),
        Metric("in_freq", 43.0, boundaries=(30, 70)),
    ]


def test_check_ups_in_freq_crit() -> None:
    section = parse_ups_in_freq([["1", "390"]])
    assert list(check_ups_in_freq("1", {"levels_lower": (45, 40)}, section)) == [
        Result(state=State.CRIT, summary="39.0 Hz (warn/crit below 45 Hz/40 Hz)"),
        Metric("in_freq", 39.0, boundaries=(30, 70)),
    ]


def test_check_ups_in_freq_item_missing() -> None:
    assert (
        list(check_ups_in_freq("9", {"levels_lower": (45, 40)}, parse_ups_in_freq([["1", "500"]])))
        == []
    )


def test_check_ups_in_freq_upper_levels_absent_keeps_legacy_behavior() -> None:
    # 56 Hz without upper levels configured must not warn.
    section = parse_ups_in_freq([["1", "560"]])
    assert list(check_ups_in_freq("1", {"levels_lower": (45, 40)}, section)) == [
        Result(state=State.OK, summary="56.0 Hz"),
        Metric("in_freq", 56.0, boundaries=(30, 70)),
    ]


def test_check_ups_in_freq_upper_warn() -> None:
    section = parse_ups_in_freq([["1", "560"]])
    assert list(
        check_ups_in_freq("1", {"levels_lower": (45, 40), "levels_upper": (55, 60)}, section)
    ) == [
        Result(state=State.WARN, summary="56.0 Hz (warn/crit above 55 Hz/60 Hz)"),
        Metric("in_freq", 56.0, levels=(55, 60), boundaries=(30, 70)),
    ]


def test_check_ups_in_freq_upper_crit() -> None:
    section = parse_ups_in_freq([["1", "620"]])
    assert list(
        check_ups_in_freq("1", {"levels_lower": (45, 40), "levels_upper": (55, 60)}, section)
    ) == [
        Result(state=State.CRIT, summary="62.0 Hz (warn/crit above 55 Hz/60 Hz)"),
        Metric("in_freq", 62.0, levels=(55, 60), boundaries=(30, 70)),
    ]


def test_check_ups_in_freq_lower_crit_still_triggers_with_upper_set() -> None:
    section = parse_ups_in_freq([["1", "380"]])
    assert list(
        check_ups_in_freq("1", {"levels_lower": (45, 40), "levels_upper": (55, 60)}, section)
    ) == [
        Result(state=State.CRIT, summary="38.0 Hz (warn/crit below 45 Hz/40 Hz)"),
        Metric("in_freq", 38.0, levels=(55, 60), boundaries=(30, 70)),
    ]


def test_check_ups_in_freq_upper_warn_at_exact_threshold() -> None:
    # freq == warn_upper triggers WARN ("above" levels use >=).
    section = parse_ups_in_freq([["1", "550"]])
    assert list(
        check_ups_in_freq("1", {"levels_lower": (45, 40), "levels_upper": (55, 60)}, section)
    ) == [
        Result(state=State.WARN, summary="55.0 Hz (warn/crit above 55 Hz/60 Hz)"),
        Metric("in_freq", 55.0, levels=(55, 60), boundaries=(30, 70)),
    ]


def test_check_ups_in_freq_upper_crit_at_exact_threshold() -> None:
    # freq == crit_upper triggers CRIT ("above" levels use >=).
    section = parse_ups_in_freq([["1", "600"]])
    assert list(
        check_ups_in_freq("1", {"levels_lower": (45, 40), "levels_upper": (55, 60)}, section)
    ) == [
        Result(state=State.CRIT, summary="60.0 Hz (warn/crit above 55 Hz/60 Hz)"),
        Metric("in_freq", 60.0, levels=(55, 60), boundaries=(30, 70)),
    ]
