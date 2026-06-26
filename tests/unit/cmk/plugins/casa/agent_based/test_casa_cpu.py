#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# mypy: disable-error-code="misc"

from collections.abc import Sequence

import pytest

from cmk.agent_based.v2 import Metric, Result, Service, State, StringTable
from cmk.plugins.casa.agent_based import casa_cpu_temp, casa_cpu_util
from cmk.plugins.casa.agent_based.casa_cpu_mem import (
    check_casa_cpu_mem,
    discover_casa_cpu_mem,
    parse_casa_cpu_mem,
)
from cmk.plugins.casa.agent_based.casa_cpu_temp import (
    check_casa_cpu_temp,
    discover_casa_cpu_temp,
    parse_casa_cpu_temp,
)
from cmk.plugins.casa.agent_based.casa_cpu_util import (
    check_casa_cpu_util,
    discover_casa_cpu_util,
    parse_casa_cpu_util,
)


@pytest.fixture(autouse=True)
def _patch_value_store(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(casa_cpu_temp, "get_value_store", dict)
    monkeypatch.setattr(casa_cpu_util, "get_value_store", dict)


# --------------------------------------------------------------------------- #
# casa_cpu_temp
# --------------------------------------------------------------------------- #

_TEMP_INFO: Sequence[StringTable] = [
    [["1", "Module 1 CPU temperature sensor"], ["2", "Module 2 CPU temperature sensor"]],
    [["1", "455"], ["2", "600"]],
    [["1", "1"], ["2", "2"]],
    [["1", "8"], ["2", "8"]],
]


def test_discover_casa_cpu_temp() -> None:
    assert sorted(
        discover_casa_cpu_temp(parse_casa_cpu_temp(_TEMP_INFO)), key=lambda s: s.item or ""
    ) == [
        Service(item="Module 1"),
        Service(item="Module 2"),
    ]


def test_check_casa_cpu_temp_ok() -> None:
    results = list(
        check_casa_cpu_temp("Module 1", {"levels": (50.0, 60.0)}, parse_casa_cpu_temp(_TEMP_INFO))
    )
    assert Result(state=State.OK, summary="Temperature: 45.5 °C") in results
    assert Metric("temp", 45.5, levels=(50.0, 60.0)) in results


def test_check_casa_cpu_temp_sensor_failure() -> None:
    # Module 2 has temp_status != "1"
    assert list(check_casa_cpu_temp("Module 2", {}, parse_casa_cpu_temp(_TEMP_INFO))) == [
        Result(state=State.CRIT, summary="Sensor failure!"),
    ]


def test_check_casa_cpu_temp_missing_item() -> None:
    assert not list(check_casa_cpu_temp("Module 99", {}, parse_casa_cpu_temp(_TEMP_INFO)))


# --------------------------------------------------------------------------- #
# casa_cpu_util
# --------------------------------------------------------------------------- #

_UTIL_INFO: Sequence[StringTable] = [
    [["1", "Module 1 QEM"], ["2", "Module 2 QEM"]],
    [["1", "42"], ["2", "0"]],
]


def test_discover_casa_cpu_util() -> None:
    assert sorted(
        discover_casa_cpu_util(parse_casa_cpu_util(_UTIL_INFO)), key=lambda s: s.item or ""
    ) == [
        Service(item="Module 1"),
        Service(item="Module 2"),
    ]


def test_check_casa_cpu_util_ok() -> None:
    results = list(check_casa_cpu_util("Module 1", {}, parse_casa_cpu_util(_UTIL_INFO)))
    assert Result(state=State.OK, summary="Total CPU: 42.00%") in results
    assert Metric("util", 42.0, boundaries=(0.0, None)) in results


def test_check_casa_cpu_util_missing_item() -> None:
    assert not list(check_casa_cpu_util("Module 99", {}, parse_casa_cpu_util(_UTIL_INFO)))


# --------------------------------------------------------------------------- #
# casa_cpu_mem
# --------------------------------------------------------------------------- #

_MEM_INFO: Sequence[StringTable] = [
    [["1", "Module 1"], ["2", "Module 2"]],
    [["1", "1000"], ["2", "2000"]],
    [["1", "500"], ["2", "1000"]],
    [["1", "0"], ["2", "0"]],
]


def test_discover_casa_cpu_mem() -> None:
    assert sorted(
        discover_casa_cpu_mem(parse_casa_cpu_mem(_MEM_INFO)), key=lambda s: s.item or ""
    ) == [
        Service(item="Module 1"),
        Service(item="Module 2"),
    ]


def test_check_casa_cpu_mem_ok() -> None:
    results = list(check_casa_cpu_mem("Module 1", {"levels": None}, parse_casa_cpu_mem(_MEM_INFO)))
    assert results[0] == Result(state=State.OK, summary="Usage: 50.00% - 500 B of 1000 B")
    assert Metric("memused", 500.0, boundaries=(0.0, 1000.0)) in results


def test_check_casa_cpu_mem_abs_levels() -> None:
    results = list(
        check_casa_cpu_mem("Module 1", {"levels": (400, 800)}, parse_casa_cpu_mem(_MEM_INFO))
    )
    assert isinstance(results[0], Result)
    assert results[0].state == State.WARN


def test_check_casa_cpu_mem_missing_item() -> None:
    assert not list(
        check_casa_cpu_mem("Module 99", {"levels": None}, parse_casa_cpu_mem(_MEM_INFO))
    )
