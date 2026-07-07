#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest
from pydantic import ValidationError

from cmk.agent_based.v3_unstable import (
    AggregatedInstantGauge,
    AggregatedInstantHistogram,
    AggregatedInstantSum,
    AggregationTemporality,
    CustomMetricMeta,
    MetricsRecord,
    MetricType,
)


def _metadata(metric_type: MetricType) -> CustomMetricMeta:
    return CustomMetricMeta(
        series_id="series-1",
        metric_type=metric_type,
        name="the_metric",
        description="A metric",
        resource_attributes={"resource_key": "resource_value"},
        scope_name="scope",
        scope_version="1.0",
        scope_attributes={"scope_key": "scope_value"},
        attributes={"datapoint_key": "datapoint_value"},
        unit="{units}",
        aggregation_temporality=AggregationTemporality.DELTA,
        is_monotonic=True,
    )


RECORDS = [
    MetricsRecord(
        filter_name="the_filter",
        metadata=_metadata(MetricType.GAUGE),
        data=AggregatedInstantGauge(series_id="series-1", value=42.0),
    ),
    MetricsRecord(
        filter_name="the_filter",
        metadata=_metadata(MetricType.SUM),
        data=AggregatedInstantSum(series_id="series-1", value_delta=7.0, rate=0.5),
    ),
    MetricsRecord(
        filter_name="the_filter",
        metadata=_metadata(MetricType.HISTOGRAM),
        data=AggregatedInstantHistogram(
            series_id="series-1",
            count_delta=13,
            count_rate=1.3,
            sum_delta=99.9,
            values_at_quantiles=[0.5, 0.9],
        ),
    ),
]


def test_round_trip() -> None:
    assert [
        MetricsRecord.model_validate_json(record.model_dump_json()) for record in RECORDS
    ] == RECORDS


def test_data_discrimination() -> None:
    gauge, sum_, histogram = (
        MetricsRecord.model_validate_json(record.model_dump_json()) for record in RECORDS
    )
    assert isinstance(gauge.data, AggregatedInstantGauge)
    assert isinstance(sum_.data, AggregatedInstantSum)
    assert isinstance(histogram.data, AggregatedInstantHistogram)


def test_invalid_record_raises() -> None:
    with pytest.raises(ValidationError):
        MetricsRecord.model_validate_json("{}")
