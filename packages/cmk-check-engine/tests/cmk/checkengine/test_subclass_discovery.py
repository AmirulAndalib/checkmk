#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import importlib
import sys
from collections.abc import Iterator, Mapping
from pathlib import Path
from types import ModuleType

import pytest

from cmk.checkengine.subclass_discovery import (
    discover,
    DuplicateIdentifierError,
    get_default_identifier,
)


def _make_package(root_dir: Path, pkg_name: str, files: Mapping[str, str]) -> ModuleType:
    pkg_dir = root_dir / pkg_name
    for rel, content in files.items():
        target = pkg_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    importlib.invalidate_caches()
    return importlib.import_module(pkg_name)


@pytest.fixture
def fixture_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    monkeypatch.syspath_prepend(str(tmp_path))
    imported_before = set(sys.modules)
    yield tmp_path
    # Drop the fixture packages so a later test may reuse a package name.
    for name in set(sys.modules) - imported_before:
        del sys.modules[name]


def test_discover_ignores_merely_imported_and_keeps_reexports(fixture_root: Path) -> None:
    root = _make_package(
        fixture_root,
        "disc_fixture_ok",
        {
            "__init__.py": "",
            "base.py": "class Base: pass\n",
            # Private top-level module: skipped by discovery, must not leak in via an import.
            "_hidden.py": "from .base import Base\n\n\nclass Hidden(Base): pass\n",
            # Public module that *imports* Hidden (must not be registered here) and *defines* Visible.
            "visible.py": (
                "from .base import Base\n"
                "from ._hidden import Hidden\n\n\n"
                "class Visible(Base): pass\n"
            ),
            # Package that re-exports a class defined in a private submodule (the SNMPFetcher pattern).
            "pkg_reexport/__init__.py": "from ._impl import Packaged as Packaged\n",
            "pkg_reexport/_impl.py": "from ..base import Base\n\n\nclass Packaged(Base): pass\n",
        },
    )
    base = importlib.import_module("disc_fixture_ok.base").Base

    result = discover(root, base, get_default_identifier)

    assert set(result) == {"Visible", "Packaged"}
    # The merely-imported (and privately-defined) class is not registered.
    assert "Hidden" not in result
    # The re-export from a private submodule is registered, owned by its defining submodule.
    assert result["Packaged"].__module__ == "disc_fixture_ok.pkg_reexport._impl"


def test_discover_raises_on_duplicate_identifier(fixture_root: Path) -> None:
    root = _make_package(
        fixture_root,
        "disc_fixture_dup",
        {
            "__init__.py": "",
            "base.py": "class Base: pass\n",
            "mod_a.py": "from .base import Base\n\n\nclass AlphaThing(Base): pass\n",
            "mod_b.py": "from .base import Base\n\n\nclass BetaThing(Base): pass\n",
        },
    )
    base = importlib.import_module("disc_fixture_dup.base").Base

    with pytest.raises(DuplicateIdentifierError):
        discover(root, base, lambda _cls: "collision")
