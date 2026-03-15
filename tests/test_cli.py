"""
CLI-level tests for fastapi-seed.

These tests use Typer's CliRunner to invoke the CLI in-process
and mock.patch to simulate missing system tools — no real installs
or uninstalls needed.
"""

from unittest.mock import patch

from typer.testing import CliRunner

from fastapi_seed.cli import app

runner = CliRunner()


def test_uv_not_installed_shows_error():
    with patch("fastapi_seed.cli.shutil.which", return_value=None):
        result = runner.invoke(app, ["init", "my-project"])
    assert result.exit_code == 1
    assert "uv is not installed" in result.output


def test_git_not_installed_shows_error():
    def fake_which(cmd):
        return None if cmd == "git" else "/usr/bin/uv"

    with patch("fastapi_seed.cli.shutil.which", fake_which):
        result = runner.invoke(app, ["init", "my-project"])
    assert result.exit_code == 1
    assert "git is not installed" in result.output
