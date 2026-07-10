#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping

from cmk.server_side_calls.v1 import EnvProxy, NoProxy, URLProxy

# note: being more specific here will just cause trouble when passing to requests.
ProxyConfig = None | Mapping[str, str]


def deserialize_proxy_config(serialized_config: str | None) -> ProxyConfig:
    match serialized_config:
        case "FROM_ENVIRONMENT" | None:
            return None
        case "NO_PROXY":
            return {"http": "", "https": ""}
        case str(url):
            return {"http": url, "https": url}


def serialize_proxy(proxy: NoProxy | EnvProxy | URLProxy) -> str:
    match proxy:
        case URLProxy(url=url):
            return url
        case EnvProxy():
            return "FROM_ENVIRONMENT"
        case NoProxy():
            return "NO_PROXY"
