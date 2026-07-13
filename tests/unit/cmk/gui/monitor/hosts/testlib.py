#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Sequence

from polyfactory.factories import DataclassFactory

from cmk.gui.monitor.hosts._models import Host, HostFilter, HostSort
from cmk.gui.monitor.hosts._repositories import HostRepository


class HostFactory(DataclassFactory[Host]):
    __check_model__ = False


def get_fake_host_repository(*, n_hosts: int) -> HostRepository:
    class HostFakeRepository:
        def __init__(self) -> None:
            self._hosts = [HostFactory.build() for _ in range(n_hosts)]

        def fetch(
            self,
            *,
            limit: int,
            query: str,
            sorters: Sequence[HostSort],
            filters: HostFilter,
        ) -> Sequence[Host]:
            return self._hosts[:limit]

        def count_total(self) -> int:
            return len(self._hosts)

        def count_matched(self, *, query: str, filters: HostFilter) -> int:
            # Not implementing this as we don't need to test a fake implementation of this.
            return self.count_total()

    return HostFakeRepository()
