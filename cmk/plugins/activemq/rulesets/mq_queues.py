#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    InputHint,
    Integer,
    LevelDirection,
    migrate_to_integer_simple_levels,
    SimpleLevels,
    String,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _migrate(params: object) -> Mapping[str, object]:
    """Migrate the legacy consumerCount levels to separate upper/lower level fields.

    The legacy consumerCount tuple (warn, crit) is interpreted as:
    - upper levels if crit > warn
    - lower levels if warn > crit

    Conversion of the individual level tuples to the SimpleLevels model is left to the
    per-element ``migrate`` (``migrate_to_integer_simple_levels``).
    """
    if not isinstance(params, dict):
        raise TypeError(params)
    migrated = dict(params)
    match migrated.pop("consumerCount", None):
        case (int(warn), int(crit)) as levels:
            direction = "upper" if crit > warn else "lower"
            migrated.setdefault(f"consumer_count_levels_{direction}", levels)
        case _:
            pass
    return migrated


def _parameter_form() -> Dictionary:
    return Dictionary(
        migrate=_migrate,
        elements={
            "size": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for the queue length"),
                    help_text=Help(
                        "Queue length refers to the total number of messages that have "
                        "not been acknowledged by a consumer."
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    migrate=migrate_to_integer_simple_levels,
                    prefill_fixed_levels=InputHint((0, 0)),
                ),
            ),
            "consumer_count_levels_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for the consumer count"),
                    help_text=Help(
                        "Consumer count is the number of connected consumers to a queue"
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    migrate=migrate_to_integer_simple_levels,
                    prefill_fixed_levels=InputHint((0, 0)),
                ),
            ),
            "consumer_count_levels_lower": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Lower levels for the consumer count"),
                    help_text=Help(
                        "Consumer count is the number of connected consumers to a queue"
                    ),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Integer(),
                    migrate=migrate_to_integer_simple_levels,
                    prefill_fixed_levels=InputHint((0, 0)),
                ),
            ),
        },
    )


rule_spec_mq_queues = CheckParameters(
    name="mq_queues",
    title=Title("Apache ActiveMQ queue lengths"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form,
    condition=HostAndItemCondition(
        item_title=Title("Queue Name"),
        item_form=String(help_text=Help("The name of the queue like in the Apache queue manager")),
    ),
)
