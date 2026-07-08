#!/usr/bin/env bash
# Reclaim this worktree's Bazel output base on paseo teardown.
# `bazel clean --expunge` fails on rules_js's read-only pnpm dirs and orphans
# the base, so resolve it, restore write perms, stop the server, and remove it.
set -u

worktree="${PASEO_WORKTREE_PATH:-$PWD}"

# bazel info may be preceded by wrapper/progress output; keep only the path line.
output_base="$(cd "$worktree" && bazel info output_base 2>/dev/null | grep -m1 '^/')"

if [ -n "$output_base" ] && [ -d "$output_base" ]; then
    chmod -R u+w "$output_base" 2>/dev/null || true
    (cd "$worktree" && bazel shutdown 2>/dev/null) || true
    rm -rf "$output_base"
fi
