"""Unit tests for EmailState and state management functions.

These tests verify the core LangGraph state management concepts:
- State creation and initialization
- State immutability
- Partial state updates
- State formatting for display
"""

from datetime import datetime
from typing import Literal

import pytest

from email_assistant.models.state import (
    EmailState,
    create_initial_state,
    format_state_display,
    update_state,
)


class TestEmailState:
    """Test the EmailState TypedDict structure."""

    def test_create_email_state_with_all_fields(self) -> None:
        """Test creating an EmailState with all fields populated."""
        now = datetime.now()
        state: EmailState = {
            "subject": "Test Subject",
            "body": "Test Body",
            "recipient": "test@example.com",
            "email_type": "business",
            "created_at": now,
            "modified_at": now,
            "metadata": {"key": "value"},
        }

        assert state["subject"] == "Test Subject"
        assert state["body"] == "Test Body"
        assert state["recipient"] == "test@example.com"
        assert state["email_type"] == "business"
        assert state["created_at"] == now
        assert state["modified_at"] == now
        assert state["metadata"] == {"key": "value"}

    def test_create_email_state_with_optional_fields_none(self) -> None:
        """Test creating an EmailState with optional fields as None."""
        state: EmailState = {
            "subject": "Test",
            "body": "Body",
            "recipient": "user@test.com",
            "email_type": "personal",
            "created_at": None,
            "modified_at": None,
            "metadata": None,
        }

        assert state["created_at"] is None
        assert state["modified_at"] is None
        assert state["metadata"] is None


class TestCreateInitialState:
    """Test the create_initial_state helper function."""

    def test_create_default_state(self) -> None:
        """Test creating state with default values."""
        state = create_initial_state()

        assert state["subject"] == ""
        assert state["body"] == ""
        assert state["recipient"] == ""
        assert state["email_type"] == "other"
        assert state["created_at"] is not None
        assert state["modified_at"] is not None
        assert state["metadata"] == {}

    def test_create_state_with_values(self) -> None:
        """Test creating state with specific values."""
        state = create_initial_state(
            subject="Hello World",
            body="This is a test email.",
            recipient="recipient@example.com",
            email_type="support",
        )

        assert state["subject"] == "Hello World"
        assert state["body"] == "This is a test email."
        assert state["recipient"] == "recipient@example.com"
        assert state["email_type"] == "support"
        assert isinstance(state["created_at"], datetime)
        assert isinstance(state["modified_at"], datetime)
        assert state["metadata"] == {}

    def test_timestamps_are_set(self) -> None:
        """Test that timestamps are automatically set."""
        before = datetime.now()
        state = create_initial_state()
        after = datetime.now()

        assert state["created_at"] is not None
        assert state["modified_at"] is not None
        assert before <= state["created_at"] <= after
        assert before <= state["modified_at"] <= after
        assert state["created_at"] == state["modified_at"]


class TestUpdateState:
    """Test the update_state function for immutable updates."""

    def test_update_single_field(self) -> None:
        """Test updating a single field maintains immutability."""
        initial = create_initial_state(subject="Original")
        updated = update_state(initial, subject="Updated")

        assert initial["subject"] == "Original"
        assert updated["subject"] == "Updated"
        assert id(initial) != id(updated)

    def test_update_multiple_fields(self) -> None:
        """Test updating multiple fields at once."""
        initial = create_initial_state()
        updated = update_state(
            initial,
            subject="New Subject",
            body="New Body",
            recipient="new@example.com",
        )

        assert updated["subject"] == "New Subject"
        assert updated["body"] == "New Body"
        assert updated["recipient"] == "new@example.com"
        assert updated["email_type"] == initial["email_type"]

    def test_update_modifies_timestamp(self) -> None:
        """Test that updates change the modified_at timestamp."""
        initial = create_initial_state()
        import time

        time.sleep(0.01)

        updated = update_state(initial, subject="Changed")

        # Both timestamps should exist since create_initial_state sets them
        assert updated["modified_at"] is not None
        assert initial["modified_at"] is not None
        assert updated["modified_at"] > initial["modified_at"]
        assert updated["created_at"] == initial["created_at"]

    def test_empty_update_preserves_state(self) -> None:
        """Test that empty updates don't change the state."""
        initial = create_initial_state(subject="Test")
        updated = update_state(initial)

        assert updated["subject"] == initial["subject"]
        assert updated["modified_at"] == initial["modified_at"]

    def test_update_metadata(self) -> None:
        """Test updating the metadata field."""
        initial = create_initial_state()
        metadata = {"processed": True, "node": "test_node"}
        updated = update_state(initial, metadata=metadata)

        assert updated["metadata"] == metadata
        assert initial["metadata"] == {}


class TestFormatStateDisplay:
    """Test the format_state_display function."""

    def test_format_empty_state(self) -> None:
        """Test formatting state with empty fields."""
        state = create_initial_state()
        output = format_state_display(state)

        assert "EmailState Contents:" in output
        assert "Subject: (empty)" in output
        assert "Recipient: (empty)" in output
        assert "Body: (empty)" in output
        assert "Email Type: other" in output

    def test_format_populated_state(self) -> None:
        """Test formatting state with populated fields."""
        state = create_initial_state(
            subject="Test Subject",
            body="Test Body Content",
            recipient="user@example.com",
            email_type="business",
        )
        output = format_state_display(state)

        assert "Subject: Test Subject" in output
        assert "Body: Test Body Content" in output
        assert "Recipient: user@example.com" in output
        assert "Email Type: business" in output
        assert "Created:" in output
        assert "Modified:" in output

    def test_format_state_with_metadata(self) -> None:
        """Test formatting state that includes metadata."""
        state = create_initial_state()
        state = update_state(state, metadata={"key": "value", "count": 42})
        output = format_state_display(state)

        assert "Metadata: {'key': 'value', 'count': 42}" in output

    def test_format_state_without_timestamps(self) -> None:
        """Test formatting state without timestamps."""
        state: EmailState = {
            "subject": "Test",
            "body": "Body",
            "recipient": "test@test.com",
            "email_type": "personal",
            "created_at": None,
            "modified_at": None,
            "metadata": None,
        }
        output = format_state_display(state)

        assert "Created:" not in output
        assert "Modified:" not in output
        assert "Metadata:" not in output


@pytest.mark.parametrize(
    "email_type",
    ["business", "personal", "support", "other"],
)
def test_email_type_values(
    email_type: Literal["business", "personal", "support", "other"],
) -> None:
    """Test that all email_type values are accepted."""
    state = create_initial_state(email_type=email_type)
    assert state["email_type"] == email_type
