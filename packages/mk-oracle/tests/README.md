# mk-oracle Tests

Tests for the `mk-oracle` agent plugin, most of which drive a real Oracle database.
The suite is endpoint-driven: connection targets come from environment variables, not hard-coded hosts.
This document covers how those endpoints are configured and how to run the tests — including validating the **Windows** binary against a **locally installed** Oracle host over SSH.

## Layout

- `test_ora_sql.rs` — main integration suite; connects to every endpoint in `WORKING_ENDPOINTS` and exercises sections, discovery, PDB handling, and custom metrics.
- `test_mk_oracle_bin.rs` — drives the built binary end-to-end (CLI behaviour, agent output).
- `common/tools.rs` — helpers that build mini `Config`s from an endpoint and, on Windows, patch `PATH`/`TNS_ADMIN` to the bundled OCI runtime.
- `files/` — fixtures: `endpoints.txt`, TNS config under `tns/`, docker compose under `docker/`, and the `test-*.yml` configs.
- `perf/`, `regression/` — performance and regression fixtures.

## Database endpoints

Two environment variables select the databases under test:

| Variable          | Required | Meaning                                                                                    |
| ----------------- | -------- | ------------------------------------------------------------------------------------------ |
| `CI_ORA2_DB_TEST` | Yes      | External reference endpoint; the suite unwraps it and treats it as `WORKING_ENDPOINTS[0]`. |
| `CI_ORA1_DB_TEST` | No       | Local endpoint; when set, local-connection tests run, otherwise they are skipped.          |

Both use the same colon-separated connection string, parsed by `SqlDbEndpoint::from_str`:

```
host:user:password:port:instance_name:role:service_name:sid:_:_
```

| Field               | Notes                                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------------------- |
| `host`              | DNS name or IP.                                                                                               |
| `user` / `password` | DB credentials. May be left empty to reuse the previous endpoint's credentials.                               |
| `port`              | Listener port (default `1521`).                                                                               |
| `instance_name`     | `_` or empty → `None`. Used to verify the plugin identifies the instance.                                     |
| `role`              | e.g. `sysdba`; empty → none. `localhost` endpoints connect as `sysdba` automatically (see `common/tools.rs`). |
| `service_name`      | Mandatory for connection.                                                                                     |
| `sid`               | `_` or empty → `None`.                                                                                        |

`files/endpoints.txt` lists the endpoints to load.
It references `$CI_ORA2_DB_TEST` only, so pointing that variable at any reachable database is sufficient — no edits to the file are needed for a local run.
CI delivers only a password, so `CI_ORA2_DB_TEST` is constructed from it in the run scripts and the Jenkins jobs.

> Never commit a connection string containing credentials.
> Build the string from a password held in an environment variable or a `0600` file outside the checkout.

## Running the tests

By default both flows connect **over the network** to the shared Rocky-Linux CI DB. The dedicated Windows job overrides the target to the Windows-native DB (see below).

**Linux** — via Bazel:

```bash
bazel test //packages/mk-oracle:mk-oracle-lib-test-internal   # unit tests, no DB
bazel test //packages/mk-oracle:mk-oracle-lib-test-external   # component tests, needs a DB + OCI client
```

The component tests need the Oracle Instant Client staged under `runtimes/`; the package's `run` script orchestrates that and constructs `CI_ORA2_DB_TEST` for `oracle-rocky-ci.lan.checkmk.net` from `CI_ORA_TEST_PASSWORD`.

**Windows** — `run.ps1 --component-tests` builds the `x86_64-pc-windows-msvc` target and runs the suite.
By default it constructs `CI_ORA2_DB_TEST` for the Rocky DB from `CI_ORA_TEST_PASSWORD`, exactly as on Linux.
The `winagt-test-mk-oracle` job overrides `CI_ORA2_DB_TEST` to the Windows-native Oracle 23ai Free on `oracle-win-ci.lan.checkmk.net`, using its `CI_ORA_WIN_TEST_PASSWORD` credential — so that job exercises the Windows agent against a Windows-hosted DB while the shared build jobs keep using Rocky.

## Validating the Windows binary against a local Oracle host

The default Windows job runs the binary on a build node and connects **over the network** to `oracle-win-ci.lan.checkmk.net`.
Even against a Windows-native DB, a network connection never touches the host-local paths a co-located agent uses: local `sysdba`/bequeath connections and registry-based instance discovery (`HKLM\SOFTWARE\ORACLE`).
To cover those, run the Windows test binary **on** a Windows Oracle host and point it at `localhost`.

This is a manual procedure; it is not yet wired into CI.

### 1. SSH to the host without leaving a key behind

Password auth plus connection multiplexing authenticates once, interactively, then reuses the socket — no `authorized_keys` entry on the host and no password in later commands.

`~/.ssh/config`:

```
Host oracle-win-ci
    HostName 10.200.0.141
    User administrator
    PubkeyAuthentication no
    PreferredAuthentications password,keyboard-interactive
    ControlMaster auto
    ControlPath ~/.ssh/cm-%r@%h-%p
    ControlPersist 30m
```

```bash
# open the master once (prompts for the password, entered locally, never stored):
ssh oracle-win-ci -O check 2>/dev/null || ssh -fN oracle-win-ci
# reuse it with no password (you or tooling):
ssh oracle-win-ci 'powershell -c "reg query HKLM\SOFTWARE\ORACLE /s"'
# tear down when done:
ssh oracle-win-ci -O exit
```

The host needs `sshd` running and port 22 open.
If you prefer key auth instead, note that Windows OpenSSH ignores per-user `authorized_keys` for administrators — install the public key into `C:\ProgramData\ssh\administrators_authorized_keys` and restrict its ACL to `Administrators` and `SYSTEM`.

### 2. Build the test binary

On a Windows host with the toolchain (e.g. the existing `winagt` node):

```powershell
cargo test --release --target x86_64-pc-windows-msvc --no-run
# → target\x86_64-pc-windows-msvc\release\deps\test_ora_sql-<hash>.exe
```

### 3. Stage on the Oracle host

Copy the executable and the `tests/files/` tree (the binary resolves fixtures relative to the working directory) into one directory on the host, preserving the `tests\files\...` layout.

### 4. Run against the local instances

Point both endpoints at `localhost` and use the installed Oracle client via `ORACLE_HOME`:

```powershell
$pw = "<system-password>"
$env:CI_ORA2_DB_TEST = "localhost:system:${pw}:1521:_::FREE:FREE:_:"
$env:CI_ORA1_DB_TEST = "localhost:system:${pw}:1521:_::FREEPDB1:_:_:"
$env:ORACLE_HOME     = "C:\oracle\26ai\dbhomeFree"
$env:PATH            = "$env:ORACLE_HOME\bin;$env:PATH"
.\test_ora_sql-<hash>.exe --test-threads=4
```

Connection strings for a host with both a 23ai Free and a 19c instance installed:

| Instance             | Port | service_name | sid      | Connection string                                |
| -------------------- | ---- | ------------ | -------- | ------------------------------------------------ |
| 23ai Free (CDB root) | 1521 | `FREE`       | `FREE`   | `localhost:system:<pw>:1521:_::FREE:FREE:_:`     |
| 23ai Free (PDB)      | 1521 | `FREEPDB1`   | —        | `localhost:system:<pw>:1521:_::FREEPDB1:_:_:`    |
| 19c (CDB root)       | 1522 | `orcl19`     | `ORCL19` | `localhost:system:<pw>:1522:_::orcl19:ORCL19:_:` |
| 19c (PDB)            | 1522 | `orcl19pdb`  | —        | `localhost:system:<pw>:1522:_::orcl19pdb:_:_:`   |

## Troubleshooting

- `ORA-12170` (TNS connect timeout) — the port is filtered; check the host firewall and that the listener binds a reachable address, not `127.0.0.1`.
- `ORA-01017` (invalid username/password) — reachable, wrong credentials.
- `ORA-12514` (service not known) — wrong `service_name`; confirm with `lsnrctl status` on the host.
- SSH hangs — port 22 blocked; SSH prompts for a password on reuse — the ControlMaster socket is not open, or (key auth) the `administrators_authorized_keys` ACL is wrong.
- `No local endpoint found` in test output — `CI_ORA1_DB_TEST` is unset; local-connection tests are skipped.
