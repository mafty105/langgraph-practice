"""Pytest configuration and fixtures."""

import pytest
from typer.testing import CliRunner


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a CLI runner for testing Typer applications."""
    return CliRunner()
