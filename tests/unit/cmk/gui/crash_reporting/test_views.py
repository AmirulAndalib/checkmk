#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from cmk.gui.crash_reporting.views import PainterCrashException


@pytest.mark.parametrize(
    "exc_type, exc_value, expected",
    [
        pytest.param(
            "ValueError",
            "invalid literal",
            "ValueError: invalid literal",
            id="plain single line",
        ),
        pytest.param(
            "MKAutomationException",
            "Error running automation call <tt>bake-agents</tt> (exit code 2), error: "
            "<pre>[ERROR] Execution of automation 'bake-agents' failed\n"
            "Traceback (most recent call last):\n"
            '  File "automations.py", line 116, in _execute\n'
            "OSError: [Errno 2] No such file or directory</pre>",
            "MKAutomationException: Error running automation call bake-agents (exit code 2), "
            "error: [ERROR] Execution of automation 'bake-agents' failed",
            id="html markup and multi-line traceback collapse to first line",
        ),
        pytest.param(
            "RuntimeError",
            "\n\n  boom  \n\nsecond line",
            "RuntimeError: boom",
            id="leading blank lines skipped and trimmed",
        ),
        pytest.param(
            "RuntimeError",
            "",
            "RuntimeError: ",
            id="empty value",
        ),
    ],
)
def test_painter_crash_exception_summarize(exc_type: str, exc_value: str, expected: str) -> None:
    summary = PainterCrashException.summarize(exc_type, exc_value)
    assert summary == expected
    assert "\n" not in summary
    assert "<" not in summary
