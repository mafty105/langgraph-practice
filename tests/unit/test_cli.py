"""Unit tests for CLI module."""

from typer.testing import CliRunner

from email_assistant.cli import app


def test_version_flag(cli_runner: CliRunner) -> None:
    """Test --version flag displays version correctly."""
    result = cli_runner.invoke(app, ["main", "--version"])
    assert result.exit_code == 0
    assert "Email Assistant CLI v0.1.0" in result.stdout


def test_main_command(cli_runner: CliRunner) -> None:
    """Test main command runs without errors."""
    result = cli_runner.invoke(app, ["main"])
    assert result.exit_code == 0
    assert "Welcome to Email Assistant CLI!" in result.stdout


def test_state_demo_command(cli_runner: CliRunner) -> None:
    """Test state-demo command demonstrates state management."""
    result = cli_runner.invoke(app, ["state-demo"])
    assert result.exit_code == 0

    assert "LangGraph State Management Demo" in result.stdout
    assert "Step 1: Creating initial state" in result.stdout
    assert "Step 2: Updating state immutably" in result.stdout
    assert "Step 3: Demonstrating partial updates" in result.stdout

    assert "Initial State" in result.stdout
    assert "Updated State" in result.stdout
    assert "State with Metadata" in result.stdout

    assert "Welcome to LangGraph" in result.stdout
    assert "Updated: Learning LangGraph State Management" in result.stdout

    assert "✓ State Demo Complete!" in result.stdout
    assert "Key Takeaways:" in result.stdout
