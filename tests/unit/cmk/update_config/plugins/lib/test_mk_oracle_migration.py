#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.update_config.plugins.lib.mk_oracle_migration import convert, dump


def test_empty_body_is_not_deployed() -> None:
    assert dump(convert({}).rule)["deploy"] == ("do_not_deploy", None)


def test_empty_body_auth_is_wallet() -> None:
    assert dump(convert({}).rule)["main"]["auth"] == {"auth_type": ("wallet", None)}


def test_empty_body_has_no_instances() -> None:
    assert dump(convert({}).rule)["instances"] == []


def test_empty_body_has_warning() -> None:
    assert convert({}).warnings == ["No auth defined in legacy rule. Defaulting to Oracle wallet."]


def test_deploy_when_activated_true() -> None:
    assert dump(convert({"activated": True}).rule)["deploy"] == ("deploy", None)


def test_do_not_deploy_when_activated_false() -> None:
    assert dump(convert({"activated": False}).rule)["deploy"] == ("do_not_deploy", None)


def test_async_interval_cache_age() -> None:
    assert dump(convert({"async_interval": 600}).rule)["main"]["cache_age"] == 600
