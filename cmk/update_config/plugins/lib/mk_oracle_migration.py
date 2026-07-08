#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping
from typing import Any, Literal, NamedTuple

from cmk.plugins.oracle.bakery.mk_oracle_unified import (
    GuiAuthConf,
    GuiConfig,
    GuiConnectionConf,
    GuiInstanceConf,
    GuiMainConf,
    OracleAuthType,
)

RawSecret = tuple[
    Literal["cmk_postprocessed"],
    Literal["explicit_password", "stored_password"],
    tuple[str, str],
]


class MigratedRule(NamedTuple):
    rule: GuiConfig[RawSecret]
    warnings: list[str]


def convert(legacy: Mapping[str, Any]) -> MigratedRule:
    warnings: list[str] = []
    instances: list[GuiInstanceConf[RawSecret]] = []

    deploy: tuple[Literal["deploy", "do_not_deploy"], None] = (
        ("deploy", None) if legacy.get("activated") else ("do_not_deploy", None)
    )

    cache_age = legacy.get("async_interval") or None

    auth = GuiAuthConf[RawSecret](auth_type=(OracleAuthType.WALLET, None))
    warnings.append("No auth defined in legacy rule. Defaulting to Oracle wallet.")

    main = GuiMainConf[RawSecret](auth=auth, connection=GuiConnectionConf(), cache_age=cache_age)

    return MigratedRule(
        rule=GuiConfig[RawSecret](deploy=deploy, instances=instances, main=main),
        warnings=warnings,
    )


def dump(config: GuiConfig[RawSecret]) -> dict[str, Any]:
    return config.model_dump(exclude_defaults=True, exclude_none=True, mode="python")
