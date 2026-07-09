# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

"""Unit tests for the config deployer (_copy_dir, _install_files)."""

from __future__ import annotations

import os
from pathlib import Path

from cmk.dev_deploy.deployers.config_deployer import _copy_dir, _install_files
from cmk.dev_deploy.types import ConfigDeploySpec, ConfigFileEntry, DeployMethod


def _spec(
    *,
    source_prefix: str,
    site_dest: str,
    files: tuple[ConfigFileEntry, ...],
    method: DeployMethod = DeployMethod.COPY_DIR,
    delete_extra: bool = False,
) -> ConfigDeploySpec:
    return ConfigDeploySpec(
        source_prefix=source_prefix,
        site_dest=site_dest,
        method=method,
        mode=None,
        includes=(),
        files=files,
        delete_extra=delete_extra,
        file_chmod=None,
    )


class TestCopyDirRenames:
    """Destinations must follow entry.dest, which carries pkg_files renames."""

    def test_renamed_file_deploys_under_packaged_name(self, tmp_path: Path) -> None:
        """bin/check_mk.py is packaged as bin/check_mk — never as check_mk.py."""
        repo = tmp_path / "repo"
        (repo / "bin").mkdir(parents=True)
        (repo / "bin" / "check_mk.py").write_text("#!/usr/bin/env python3\n")
        site_bin = tmp_path / "site" / "bin"

        spec = _spec(
            source_prefix="bin/",
            site_dest="bin/",
            files=(ConfigFileEntry(src="bin/check_mk.py", dest="bin/check_mk", mode="0755"),),
        )
        _copy_dir(repo / "bin", site_bin, spec, repo)

        assert (site_bin / "check_mk").read_text() == "#!/usr/bin/env python3\n"
        assert os.stat(site_bin / "check_mk").st_mode & 0o777 == 0o755
        assert not (site_bin / "check_mk.py").exists()

    def test_src_outside_source_prefix_deploys_to_dest(self, tmp_path: Path) -> None:
        """A file whose src lives outside source_prefix still lands at its dest."""
        repo = tmp_path / "repo"
        (repo / "cmk" / "utils" / "password_store").mkdir(parents=True)
        (repo / "cmk" / "utils" / "password_store" / "cli.py").write_text("cli")
        site_bin = tmp_path / "site" / "bin"

        spec = _spec(
            source_prefix="cmk/utils/password_store/",
            site_dest="bin/",
            files=(
                ConfigFileEntry(
                    src="cmk/utils/password_store/cli.py", dest="bin/cmk-pwstore", mode="0755"
                ),
            ),
        )
        _copy_dir(repo / "cmk" / "utils" / "password_store", site_bin, spec, repo)

        assert (site_bin / "cmk-pwstore").read_text() == "cli"
        assert not (site_bin / "cli.py").exists()

    def test_dest_subdirectories_are_preserved(self, tmp_path: Path) -> None:
        repo = tmp_path / "repo"
        (repo / "agents" / "plugins").mkdir(parents=True)
        (repo / "agents" / "plugins" / "mk_docker.py").write_text("plugin")
        dest = tmp_path / "site" / "share" / "agents"

        spec = _spec(
            source_prefix="agents/",
            site_dest="share/check_mk/agents/",
            files=(
                ConfigFileEntry(
                    src="agents/plugins/mk_docker.py",
                    dest="share/check_mk/agents/plugins/mk_docker.py",
                    mode="0755",
                ),
            ),
        )
        _copy_dir(repo / "agents", dest, spec, repo)

        assert (dest / "plugins" / "mk_docker.py").read_text() == "plugin"

    def test_delete_extra_keeps_renamed_file_and_removes_stray(self, tmp_path: Path) -> None:
        """delete_extra compares against dest names, so renamed files survive."""
        repo = tmp_path / "repo"
        (repo / "bin").mkdir(parents=True)
        (repo / "bin" / "check_mk.py").write_text("new")
        site_bin = tmp_path / "site" / "bin"
        site_bin.mkdir(parents=True)
        (site_bin / "check_mk.py").write_text("stray from earlier deploy")

        spec = _spec(
            source_prefix="bin/",
            site_dest="bin/",
            files=(ConfigFileEntry(src="bin/check_mk.py", dest="bin/check_mk", mode="0755"),),
            delete_extra=True,
        )
        _copy_dir(repo / "bin", site_bin, spec, repo)

        assert (site_bin / "check_mk").read_text() == "new"
        assert not (site_bin / "check_mk.py").exists()


class TestInstallFilesRenames:
    def test_installs_under_packaged_basename(self, tmp_path: Path) -> None:
        repo = tmp_path / "repo"
        (repo / "active_checks").mkdir(parents=True)
        (repo / "active_checks" / "check_foo.py").write_text("check")
        dest = tmp_path / "site" / "lib" / "nagios" / "plugins"

        spec = _spec(
            source_prefix="active_checks/",
            site_dest="lib/nagios/plugins/",
            method=DeployMethod.INSTALL_FILES,
            files=(
                ConfigFileEntry(
                    src="active_checks/check_foo.py",
                    dest="lib/nagios/plugins/check_foo",
                    mode="0755",
                ),
            ),
        )
        count = _install_files(repo / "active_checks", dest, spec, repo)

        assert count == 1
        assert (dest / "check_foo").read_text() == "check"
        assert not (dest / "check_foo.py").exists()
