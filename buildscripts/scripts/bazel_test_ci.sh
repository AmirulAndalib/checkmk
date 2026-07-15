#!/bin/bash
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

bep_json=$(mktemp /tmp/bep_XXXXXX.json)
trap 'rm -f "$bep_json"' EXIT

# ci converts commas to spaces, restore comma separation for Bazel
_extra_filters="${BAZEL_EXTRA_TAG_FILTERS// /,}"
tag_filters="-component${_extra_filters:+,${_extra_filters}}"

RC=0
bazel test \
    --build_event_json_file="$bep_json" \
    --keep_going \
    --build_tests_only \
    --//:use_faked_artifacts=true \
    --test_tag_filters="$tag_filters" \
    "$@" || RC=$?

bep_out="$(bazel info bazel-testlogs)"/_bep_output

# Drop any stale entries restored from the hot cache: bep_to_junit only writes
# files for failing targets, so a failure it recorded in a previous run would
# otherwise survive here (bazel-testlogs lives inside the cached output base)
# and be re-collected even though the current run passed.
rm -rf "$bep_out"

bazel run //buildscripts/scripts/bep_to_junit "$bep_json" "$bep_out"

exit $RC
