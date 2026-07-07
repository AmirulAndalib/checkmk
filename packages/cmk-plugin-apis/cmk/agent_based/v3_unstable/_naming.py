#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
import string
from typing import Final

# A plug-in name must be a non-empty string consisting only
# of letters A-z, digits and the underscore.
_VALID_CHARACTERS: Final = string.ascii_letters + "_" + string.digits


def validate_name(raw: str) -> str:
    if not isinstance(raw, str):
        raise TypeError(f"Names must be non-empty strings: {raw!r}")
    if not raw:
        raise ValueError(f"Names must be non-empty strings: {raw!r}")

    if invalid := "".join(c for c in raw if c not in _VALID_CHARACTERS):
        raise ValueError(f"Invalid characters in {raw!r}: {invalid!r}")

    return raw
