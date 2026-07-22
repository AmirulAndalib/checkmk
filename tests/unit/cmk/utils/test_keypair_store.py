#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pathlib import Path

from cmk.ccc.user import UserId
from cmk.utils.keypair_store import Key, KeyId, KeypairStore


def _make_key() -> Key:
    return Key(
        certificate="cert-pem",
        private_key="key-pem",
        alias="my key",
        owner=UserId("admin"),
        date=1234567890.0,
    )


def test_save_load_roundtrip(tmp_path: Path) -> None:
    store = KeypairStore(tmp_path / "agent_signature_keys.mk", "agent_signature_keys")
    store.save({KeyId("1"): _make_key()})
    assert store.load() == {KeyId("1"): _make_key()}


def test_save_self_bootstraps_the_attribute(tmp_path: Path) -> None:
    """The persisted file must be executable without a pre-seeded namespace

    `cmk.gui.config.load_config()` executes all files below multisite.d. In
    processes without the full GUI plug-in registration (e.g.
    cmk-post-rename-site) no feature config default pre-seeds
    `agent_signature_keys`, so the file has to bootstrap the variable itself.
    """
    path = tmp_path / "agent_signature_keys.mk"
    store = KeypairStore(path, "agent_signature_keys")
    store.save({KeyId("1"): _make_key()})

    namespace: dict[str, object] = {}
    exec(compile(path.read_text(), str(path), "exec"), {}, namespace)

    assert store.parse(namespace["agent_signature_keys"]) == {  # type: ignore[arg-type]
        KeyId("1"): _make_key()
    }
