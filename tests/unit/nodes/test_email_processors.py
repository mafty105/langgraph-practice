# type: ignore
"""Unit tests for email processor nodes.

These tests verify that our basic nodes follow LangGraph principles:
1. Pure functions (deterministic output for given input)
2. Partial state updates (return only modified fields)
3. Immutability (don't modify input state)
4. Proper error handling
"""

from datetime import datetime
from unittest.mock import patch

from email_assistant.models.state import create_initial_state
from email_assistant.nodes.email_processors import (
    add_greeting_node,
    add_signature_node,
    format_subject_node,
    uppercase_subject_node,
    validate_email_node,
    word_count_node,
)


class TestFormatSubjectNode:
    """Test the format_subject_node function."""

    def test_business_email_formatting(self):
        """Test that business emails get [BUSINESS] prefix."""
        state = create_initial_state(
            subject="Quarterly Report",
            email_type="business",
        )
        result = format_subject_node(state)

        assert result == {"subject": "[BUSINESS] Quarterly Report"}
        # Verify original state is not modified (immutability)
        assert state["subject"] == "Quarterly Report"

    def test_support_email_formatting(self):
        """Test that support emails get [TICKET] prefix."""
        state = create_initial_state(
            subject="Login Issue",
            email_type="support",
        )
        result = format_subject_node(state)

        assert result == {"subject": "[TICKET] Login Issue"}

    def test_personal_email_formatting(self):
        """Test that personal emails get Personal: prefix."""
        state = create_initial_state(
            subject="Weekend Plans",
            email_type="personal",
        )
        result = format_subject_node(state)

        assert result == {"subject": "Personal: Weekend Plans"}

    def test_other_email_type_unchanged(self):
        """Test that 'other' type emails remain unchanged."""
        state = create_initial_state(
            subject="General Information",
            email_type="other",
        )
        result = format_subject_node(state)

        assert result == {"subject": "General Information"}

    def test_empty_subject_returns_empty_dict(self):
        """Test that empty subject returns empty update (no changes)."""
        state = create_initial_state(
            subject="",
            email_type="business",
        )
        result = format_subject_node(state)

        assert result == {}

    def test_partial_update_pattern(self):
        """Test that node returns only the field it modifies."""
        state = create_initial_state(
            subject="Test",
            body="Some content",
            recipient="test@example.com",
            email_type="business",
        )
        result = format_subject_node(state)

        # Should only return subject field, not other fields
        assert "subject" in result
        assert "body" not in result
        assert "recipient" not in result
        assert len(result) == 1


class TestAddGreetingNode:
    """Test the add_greeting_node function."""

    def test_business_greeting(self):
        """Test business email greeting format."""
        state = create_initial_state(
            recipient="john.doe@example.com",
            body="Meeting scheduled for tomorrow.",
            email_type="business",
        )
        result = add_greeting_node(state)

        expected_body = "Dear John Doe,\n\nMeeting scheduled for tomorrow."
        assert result == {"body": expected_body}

    def test_support_greeting(self):
        """Test support email greeting format."""
        state = create_initial_state(
            recipient="alice.smith@example.com",
            body="We'll look into this issue.",
            email_type="support",
        )
        result = add_greeting_node(state)

        expected_body = (
            "Hello Alice Smith,\n\nThank you for contacting support.\n\n"
            "We'll look into this issue."
        )
        assert result == {"body": expected_body}

    def test_personal_greeting(self):
        """Test personal email greeting format."""
        state = create_initial_state(
            recipient="bob@example.com",
            body="How have you been?",
            email_type="personal",
        )
        result = add_greeting_node(state)

        expected_body = "Hi Bob!\n\nHow have you been?"
        assert result == {"body": expected_body}

    def test_other_greeting(self):
        """Test default greeting for 'other' type."""
        state = create_initial_state(
            recipient="user@example.com",
            body="Information attached.",
            email_type="other",
        )
        result = add_greeting_node(state)

        expected_body = "Hello User,\n\nInformation attached."
        assert result == {"body": expected_body}

    def test_no_recipient_uses_default_name(self):
        """Test greeting when recipient is empty."""
        state = create_initial_state(
            recipient="",
            body="Content here.",
            email_type="business",
        )
        result = add_greeting_node(state)

        expected_body = "Dear there,\n\nContent here."
        assert result == {"body": expected_body}

    def test_preserves_existing_body(self):
        """Test that existing body content is preserved."""
        state = create_initial_state(
            recipient="test@example.com",
            body="Line 1\nLine 2\nLine 3",
            email_type="personal",
        )
        result = add_greeting_node(state)

        assert "Line 1\nLine 2\nLine 3" in result["body"]
        assert result["body"].startswith("Hi Test!")


class TestAddSignatureNode:
    """Test the add_signature_node function."""

    @patch("email_assistant.nodes.email_processors.datetime")
    def test_business_signature(self, mock_datetime):
        """Test business email signature format."""
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15"

        state = create_initial_state(
            body="Email content here.",
            email_type="business",
        )
        state["metadata"] = {"sender_name": "John Smith"}

        result = add_signature_node(state)

        expected_body = "Email content here.\n\nBest regards,\nJohn Smith\n2024-01-15"
        assert result == {"body": expected_body}

    def test_support_signature(self):
        """Test support email signature format."""
        state = create_initial_state(
            body="Your issue has been resolved.",
            email_type="support",
        )
        state["metadata"] = {"sender_name": "Support Agent"}

        result = add_signature_node(state)

        expected_body = (
            "Your issue has been resolved.\n\nSincerely,\nSupport Agent\nSupport Team"
        )
        assert result == {"body": expected_body}

    def test_personal_signature(self):
        """Test personal email signature format."""
        state = create_initial_state(
            body="See you soon!",
            email_type="personal",
        )
        state["metadata"] = {"sender_name": "Alice"}

        result = add_signature_node(state)

        expected_body = "See you soon!\n\nCheers,\nAlice"
        assert result == {"body": expected_body}

    def test_default_sender_name(self):
        """Test that default sender name is used when not in metadata."""
        state = create_initial_state(
            body="Content.",
            email_type="other",
        )

        result = add_signature_node(state)

        expected_body = "Content.\n\nRegards,\nEmail Assistant"
        assert result == {"body": expected_body}

    def test_appends_to_existing_body(self):
        """Test that signature is appended to existing body."""
        state = create_initial_state(
            body="First paragraph.\n\nSecond paragraph.",
            email_type="personal",
        )
        state["metadata"] = {"sender_name": "Bob"}

        result = add_signature_node(state)

        assert result["body"].startswith("First paragraph.\n\nSecond paragraph.")
        assert result["body"].endswith("\n\nCheers,\nBob")


class TestValidateEmailNode:
    """Test the validate_email_node function."""

    def test_valid_email_passes_validation(self):
        """Test that a complete valid email passes validation."""
        state = create_initial_state(
            subject="Test Subject",
            body="Test body content",
            recipient="valid@example.com",
            email_type="business",
        )

        result = validate_email_node(state)

        assert "metadata" in result
        validation = result["metadata"]["validation"]
        assert validation["validation_passed"] is True
        assert validation["issues"] == []

    def test_missing_recipient_fails_validation(self):
        """Test that missing recipient fails validation."""
        state = create_initial_state(
            subject="Test",
            body="Body",
            recipient="",
        )

        result = validate_email_node(state)

        validation = result["metadata"]["validation"]
        assert validation["validation_passed"] is False
        assert "Missing recipient" in validation["issues"]

    def test_invalid_email_format_fails_validation(self):
        """Test that invalid email format fails validation."""
        state = create_initial_state(
            subject="Test",
            body="Body",
            recipient="not-an-email",
        )

        result = validate_email_node(state)

        validation = result["metadata"]["validation"]
        assert validation["validation_passed"] is False
        assert "Invalid recipient email format" in validation["issues"]

    def test_missing_subject_warning(self):
        """Test that missing subject adds a warning but doesn't fail."""
        state = create_initial_state(
            subject="",
            body="Body",
            recipient="test@example.com",
        )

        result = validate_email_node(state)

        validation = result["metadata"]["validation"]
        assert "Missing subject" in validation["issues"]
        # Missing subject doesn't fail validation entirely
        assert validation["validation_passed"] is True

    def test_missing_body_warning(self):
        """Test that missing body adds a warning."""
        state = create_initial_state(
            subject="Subject",
            body="",
            recipient="test@example.com",
        )

        result = validate_email_node(state)

        validation = result["metadata"]["validation"]
        assert "Missing body" in validation["issues"]

    def test_subject_too_long_warning(self):
        """Test that overly long subject adds a warning."""
        state = create_initial_state(
            subject="x" * 201,  # 201 characters
            body="Body",
            recipient="test@example.com",
        )

        result = validate_email_node(state)

        validation = result["metadata"]["validation"]
        assert "Subject too long (>200 chars)" in validation["issues"]

    def test_body_too_long_warning(self):
        """Test that overly long body adds a warning."""
        state = create_initial_state(
            subject="Subject",
            body="x" * 50001,  # 50001 characters
            recipient="test@example.com",
        )

        result = validate_email_node(state)

        validation = result["metadata"]["validation"]
        assert "Body too long (>50000 chars)" in validation["issues"]

    def test_metadata_timestamp_added(self):
        """Test that validation timestamp is added to metadata."""
        state = create_initial_state(
            subject="Test",
            body="Body",
            recipient="test@example.com",
        )

        result = validate_email_node(state)

        validation = result["metadata"]["validation"]
        assert "validated_at" in validation
        # Should be an ISO format timestamp
        datetime.fromisoformat(validation["validated_at"])

    def test_preserves_existing_metadata(self):
        """Test that existing metadata is preserved."""
        state = create_initial_state(
            subject="Test",
            body="Body",
            recipient="test@example.com",
        )
        state["metadata"] = {"existing_key": "existing_value"}

        result = validate_email_node(state)

        assert "existing_key" in result["metadata"]
        assert result["metadata"]["existing_key"] == "existing_value"
        assert "validation" in result["metadata"]


class TestUppercaseSubjectNode:
    """Test the uppercase_subject_node function."""

    def test_converts_to_uppercase(self):
        """Test that subject is converted to uppercase."""
        state = create_initial_state(
            subject="Hello World",
        )

        result = uppercase_subject_node(state)

        assert result == {"subject": "HELLO WORLD"}

    def test_handles_mixed_case(self):
        """Test handling of mixed case input."""
        state = create_initial_state(
            subject="MiXeD CaSe TeXt",
        )

        result = uppercase_subject_node(state)

        assert result == {"subject": "MIXED CASE TEXT"}

    def test_empty_subject_returns_empty_dict(self):
        """Test that empty subject returns no updates."""
        state = create_initial_state(
            subject="",
        )

        result = uppercase_subject_node(state)

        assert result == {}

    def test_already_uppercase_unchanged(self):
        """Test that already uppercase text still returns update."""
        state = create_initial_state(
            subject="ALREADY UPPERCASE",
        )

        result = uppercase_subject_node(state)

        # Should still return the field even if unchanged
        assert result == {"subject": "ALREADY UPPERCASE"}


class TestWordCountNode:
    """Test the word_count_node function."""

    def test_counts_subject_words(self):
        """Test word counting in subject."""
        state = create_initial_state(
            subject="This is a test",
            body="",
        )

        result = word_count_node(state)

        stats = result["metadata"]["statistics"]
        assert stats["subject_word_count"] == 4
        assert stats["body_word_count"] == 0
        assert stats["total_word_count"] == 4

    def test_counts_body_words(self):
        """Test word counting in body."""
        state = create_initial_state(
            subject="",
            body="The quick brown fox jumps over the lazy dog",
        )

        result = word_count_node(state)

        stats = result["metadata"]["statistics"]
        assert stats["subject_word_count"] == 0
        assert stats["body_word_count"] == 9
        assert stats["total_word_count"] == 9

    def test_counts_both_fields(self):
        """Test word counting in both subject and body."""
        state = create_initial_state(
            subject="Email Subject Here",
            body="This is the email body with some content.",
        )

        result = word_count_node(state)

        stats = result["metadata"]["statistics"]
        assert stats["subject_word_count"] == 3
        assert stats["body_word_count"] == 8
        assert stats["total_word_count"] == 11

    def test_handles_empty_fields(self):
        """Test handling of empty subject and body."""
        state = create_initial_state(
            subject="",
            body="",
        )

        result = word_count_node(state)

        stats = result["metadata"]["statistics"]
        assert stats["subject_word_count"] == 0
        assert stats["body_word_count"] == 0
        assert stats["total_word_count"] == 0

    def test_handles_multiline_text(self):
        """Test word counting with multiline text."""
        state = create_initial_state(
            subject="Subject Line",
            body="Line one here.\nLine two here.\nLine three.",
        )

        result = word_count_node(state)

        stats = result["metadata"]["statistics"]
        assert stats["subject_word_count"] == 2
        assert stats["body_word_count"] == 8
        assert stats["total_word_count"] == 10

    def test_adds_timestamp(self):
        """Test that calculation timestamp is added."""
        state = create_initial_state(
            subject="Test",
            body="Body",
        )

        result = word_count_node(state)

        stats = result["metadata"]["statistics"]
        assert "calculated_at" in stats
        # Should be an ISO format timestamp
        datetime.fromisoformat(stats["calculated_at"])

    def test_preserves_existing_metadata(self):
        """Test that existing metadata is preserved."""
        state = create_initial_state(
            subject="Test",
            body="Body",
        )
        state["metadata"] = {"other_key": "other_value"}

        result = word_count_node(state)

        assert "other_key" in result["metadata"]
        assert result["metadata"]["other_key"] == "other_value"
        assert "statistics" in result["metadata"]


class TestNodeImmutability:
    """Test that all nodes maintain immutability principle."""

    def test_nodes_dont_modify_input_state(self):
        """Test that nodes don't modify the input state object."""
        original_state = create_initial_state(
            subject="Original Subject",
            body="Original Body",
            recipient="test@example.com",
            email_type="business",
        )
        original_state["metadata"] = {"test": "value"}

        # Create a copy to compare later
        state_copy = dict(original_state)

        # Run all nodes - they should not modify the input
        format_subject_node(original_state)
        add_greeting_node(original_state)
        add_signature_node(original_state)
        validate_email_node(original_state)
        uppercase_subject_node(original_state)
        word_count_node(original_state)

        # Original state should be unchanged
        assert original_state == state_copy
        assert original_state["subject"] == "Original Subject"
        assert original_state["body"] == "Original Body"
        assert original_state["recipient"] == "test@example.com"
        assert original_state["metadata"] == {"test": "value"}


class TestNodePureFunctions:
    """Test that nodes behave as pure functions."""

    def test_deterministic_output(self):
        """Test that same input always produces same output."""
        state = create_initial_state(
            subject="Test Subject",
            body="Test Body",
            recipient="test@example.com",
            email_type="business",
        )

        # Run each node multiple times with same input
        result1 = format_subject_node(state)
        result2 = format_subject_node(state)
        assert result1 == result2

        result1 = add_greeting_node(state)
        result2 = add_greeting_node(state)
        assert result1 == result2

        result1 = uppercase_subject_node(state)
        result2 = uppercase_subject_node(state)
        assert result1 == result2

        # Note: Some nodes use datetime.now() so they're not perfectly pure,
        # but the logic should be deterministic
