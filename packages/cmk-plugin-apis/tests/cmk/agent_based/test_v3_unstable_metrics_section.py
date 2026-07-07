#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


import dataclasses
from collections.abc import Mapping

import pytest

from cmk.agent_based.v2 import HostLabelGenerator, StringTable
from cmk.agent_based.v3_unstable import (
    GaugeAggregation,
    MetricSelector,
    MetricsSection,
)

HOST_LABEL_PARAMS = {"level": "all"}


def parse_func(_string_table: StringTable) -> dict[str, object]:
    return {"": ""}


def host_label_func(
    _params: Mapping[str, object], _section: dict[str, object]
) -> HostLabelGenerator:
    yield from ()


def test_metrics_section_instantiation() -> None:
    """
    Test that the class can be instantiated correctly and all
    attributes are set.
    """
    my_filter = MetricSelector(metric_name="cpu.load", aggregation=GaugeAggregation())
    my_filter2 = MetricSelector(metric_name="cpu.temperature", aggregation=GaugeAggregation())

    section = MetricsSection(
        name="test_section",
        selectors=[my_filter, my_filter2],
        parse_function=parse_func,
        supersedes=["old_section"],
        parsed_section_name="my_parsed_name",
        host_label_function=host_label_func,
        host_label_default_parameters=HOST_LABEL_PARAMS,
        host_label_ruleset_name="my_ruleset",
    )

    assert section.selectors[0] is my_filter
    assert section.selectors[0].metric_name == "cpu.load"
    assert section.selectors[1] is my_filter2
    assert section.selectors[1].metric_name == "cpu.temperature"
    assert section.parse_function is parse_func
    assert section.name == "test_section"
    assert section.supersedes == ["old_section"]
    assert section.parsed_section_name == "my_parsed_name"
    assert section.host_label_function is host_label_func
    assert section.host_label_default_parameters is HOST_LABEL_PARAMS
    assert section.host_label_ruleset_name == "my_ruleset"


def test_metrics_section_host_label_defaults() -> None:
    section = MetricsSection(
        name="test_section",
        selectors=[MetricSelector(metric_name="cpu.load", aggregation=GaugeAggregation())],
        parse_function=parse_func,
    )

    assert section.host_label_function is None
    assert section.host_label_default_parameters is None
    assert section.host_label_ruleset_name is None


def test_metrics_section_is_immutable() -> None:
    section = MetricsSection(
        name="test_section",
        selectors=[MetricSelector(metric_name="cpu.load", aggregation=GaugeAggregation())],
        parse_function=parse_func,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        section.name = "other_name"  # type: ignore[misc]


@pytest.mark.parametrize(
    "name",
    ["", "contains-hyphen", "contains space"],
)
def test_invalid_name(name: str) -> None:
    with pytest.raises(ValueError):
        MetricsSection(
            name=name,
            selectors=[MetricSelector(metric_name="cpu.load", aggregation=GaugeAggregation())],
            parse_function=parse_func,
        )


@pytest.mark.parametrize(
    "kwargs",
    [
        {"name": "cpu_load", "parse_function": dict},
        {
            "name": "cpu_temperature",
            "selectors": [MetricSelector(metric_name="cpu.load", aggregation=GaugeAggregation())],
        },
        {
            "parse_function": dict,
            "selectors": [MetricSelector(metric_name="cpu.load", aggregation=GaugeAggregation())],
        },
    ],
)
def test_missing_required_arguments(kwargs: dict[str, object]) -> None:
    """
    Test that instantiating without required arguments raises a TypeError.
    """
    with pytest.raises(TypeError):
        MetricsSection(**kwargs)  # type: ignore[arg-type]
