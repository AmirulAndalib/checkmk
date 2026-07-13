#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
from cmk.gui.monitor.hosts._api._list_hosts import _build_host_modes, _handle_list_hosts

from .testlib import get_fake_host_repository, HostFactory


def test_handle_list_hosts_limit_handling() -> None:
    host_repo = get_fake_host_repository(n_hosts=10)
    response = _handle_list_hosts(host_repo, limit=7)

    assert len(response.hosts) == 7
    assert response.meta.limit == 7
    assert response.meta.total == 10
    assert response.meta.matched == 10


def test_handle_list_hosts_state_label_conversion() -> None:
    host_repo = get_fake_host_repository(n_hosts=100)
    response = _handle_list_hosts(host_repo)
    host_states = [host.state for host in response.hosts]

    assert all(state in {"UP", "DOWN", "UNREACHABLE"} for state in host_states)


def test_build_host_modes_none() -> None:
    host = HostFactory.build(in_downtime=False, acknowledged=False)
    assert _build_host_modes(host) == []


def test_build_host_modes_downtime() -> None:
    host = HostFactory.build(in_downtime=True, acknowledged=False)
    modes = _build_host_modes(host)

    assert [mode.icon_name for mode in modes] == ["downtime"]
    assert modes[0].link.startswith("view.py?")
    assert "downtimes_of_host" in modes[0].link


def test_build_host_modes_acknowledged() -> None:
    host = HostFactory.build(in_downtime=False, acknowledged=True)

    assert [mode.icon_name for mode in _build_host_modes(host)] == ["ack"]


def test_build_host_modes_downtime_and_acknowledged() -> None:
    host = HostFactory.build(in_downtime=True, acknowledged=True)

    assert [mode.icon_name for mode in _build_host_modes(host)] == ["downtime", "ack"]
