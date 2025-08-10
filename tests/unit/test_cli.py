"""Unit tests for CLI module."""

from typer.testing import CliRunner

from email_assistant.cli import app


def test_version_flag(cli_runner: CliRunner) -> None:
    """Test --version flag displays version correctly."""
    result = cli_runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Email Assistant CLI v0.1.0" in result.stdout


def test_main_command(cli_runner: CliRunner) -> None:
    """Test main command runs without errors."""
    result = cli_runner.invoke(app, [])
    assert result.exit_code == 0
    assert "Welcome to Email Assistant CLI!" in result.stdout
