# mk-oracle Tests

Tests for the `mk-oracle` agent plugin, most of which drive a real Oracle database.
The suite is endpoint-driven: connection targets come from environment variables, not hard-coded hosts.
This document gives the overview and quick start; the details live in [`docs/`](docs/).

## Documentation

- [`docs/endpoints.md`](docs/endpoints.md) — the endpoint model: `CI_ORA1_DB_TEST` / `CI_ORA2_DB_TEST`, the connection-string format, and how CI constructs endpoints from credentials.
- [`docs/windows-local-testing.md`](docs/windows-local-testing.md) — manual procedure for validating the **Windows** binary against a **locally installed** Oracle host over SSH, plus troubleshooting.

## Layout

- `test_ora_sql.rs` — main integration suite; connects to every endpoint in `WORKING_ENDPOINTS` and exercises sections, discovery, PDB handling, and custom metrics.
- `test_mk_oracle_bin.rs` — drives the built binary end-to-end (CLI behaviour, agent output).
- `common/tools.rs` — helpers that build mini `Config`s from an endpoint and, on Windows, patch `PATH`/`TNS_ADMIN` to the bundled OCI runtime.
- `files/` — fixtures: `endpoints.txt`, TNS config under `tns/`, docker compose under `docker/`, and the `test-*.yml` configs.
- `perf/`, `regression/` — performance and regression fixtures.

## Running the tests

By default both flows connect **over the network** to the shared Rocky-Linux CI DB. The dedicated Windows job overrides the target to the Windows-native DB (see below).
How the target databases are selected is described in [`docs/endpoints.md`](docs/endpoints.md).

**Linux** — via Bazel:

```bash
bazel test //packages/mk-oracle:mk-oracle-lib-test-internal   # unit tests, no DB
bazel test //packages/mk-oracle:mk-oracle-lib-test-external   # component tests, needs a DB + OCI client
```

The component tests need the Oracle Instant Client staged under `runtimes/`; the package's `run` script orchestrates that and constructs `CI_ORA2_DB_TEST` for `oracle-rocky-ci.lan.checkmk.net` from `CI_ORA_TEST_PASSWORD`.

**Windows** — `run.ps1 --component-tests` builds the `x86_64-pc-windows-msvc` target and runs the suite.
By default it constructs `CI_ORA2_DB_TEST` for the Rocky DB from `CI_ORA_TEST_PASSWORD`, exactly as on Linux.
The `winagt-test-mk-oracle` job overrides `CI_ORA2_DB_TEST` to the Windows-native Oracle 23ai Free on `oracle-win-ci.lan.checkmk.net`, using its `CI_ORA_WIN_TEST_PASSWORD` credential — so that job exercises the Windows agent against a Windows-hosted DB while the shared build jobs keep using Rocky.

To exercise the host-local code paths on Windows (local `sysdba`/bequeath connections, registry discovery), see [`docs/windows-local-testing.md`](docs/windows-local-testing.md).
