#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Iterator

import pytest

import cmk.utils.paths
from cmk.ccc.site import omd_site
from cmk.gui.config import Config
from cmk.gui.userdb import effective_authentication_connections
from cmk.livestatus_client import (
    AuthenticationConnectionEntry,
    SAMLAuthenticationEntry,
    SiteConfiguration,
    SiteConfigurations,
)


@pytest.fixture(name="remote_site")
def fixture_remote_site() -> Iterator[None]:
    """Make the code believe it runs on a distributed-setup remote site."""
    cmk.utils.paths.check_mk_config_dir.mkdir(parents=True, exist_ok=True)
    distr_wato_mk = cmk.utils.paths.check_mk_config_dir / "distributed_wato.mk"
    previous = distr_wato_mk.read_bytes() if distr_wato_mk.exists() else None
    distr_wato_mk.write_text("is_distributed_setup_remote_site = True\n")
    try:
        yield
    finally:
        if previous is None:
            distr_wato_mk.unlink(missing_ok=True)
        else:
            distr_wato_mk.write_bytes(previous)


def _local_self_site(auth_connections: object) -> SiteConfiguration:
    return SiteConfiguration(
        id=omd_site(),
        alias=f"Local site {omd_site()}",
        socket=("local", None),
        disable_wato=True,
        disabled=False,
        insecure=False,
        url_prefix=f"/{omd_site()}/",
        multisiteurl="",
        persist=False,
        replicate_ec=False,
        replicate_mkps=False,
        replication=None,
        timeout=5,
        user_login=True,
        proxy=None,
        authentication_connections=auth_connections,  # type: ignore[typeddict-item]
        user_attribute_sync_connections="all",
        status_host=None,
        message_broker_port=5672,
        is_trusted=True,
    )


def test_effective_authentication_connections_on_remote_prefers_propagated_global(
    load_config: Config, remote_site: None
) -> None:
    load_config.sites = SiteConfigurations({omd_site(): _local_self_site("all")})
    propagated: list[AuthenticationConnectionEntry] = [
        (
            "saml",
            SAMLAuthenticationEntry(
                connection_id="foo",
                acs_endpoint="http://localhost/remote/check_mk/saml_acs.py?acs",
                metadata_endpoint="http://localhost/remote/check_mk/saml_metadata.py?RelayState=foo",
            ),
        )
    ]
    load_config.authentication_connections = propagated

    # The seeded local self-default ("all") must not shadow the per-site ACS URL
    # that get_site_globals() propagated into the global.
    assert effective_authentication_connections(load_config.sites[omd_site()]) == propagated


def test_effective_authentication_connections_on_central_uses_own(
    load_config: Config,
) -> None:
    own: list[AuthenticationConnectionEntry] = [("ldap", "ldap_conn")]
    load_config.sites = SiteConfigurations({omd_site(): _local_self_site(own)})
    load_config.authentication_connections = [("ldap", "propagated_but_ignored")]

    assert effective_authentication_connections(load_config.sites[omd_site()]) == own
