"""Basic LangGraph nodes for email processing.

This module contains simple nodes that demonstrate fundamental LangGraph concepts:
1. Node function signatures (state in → state out)
2. Pure functions with no side effects
3. Partial state updates
4. Immutability principles

Each node is a building block that can be composed into larger graphs.
"""

from datetime import datetime
from typing import Any

from email_assistant.models.state import EmailState


def format_subject_node(state: EmailState) -> dict[str, Any]:
    """
    Format the email subject based on email type.

    This node demonstrates:
    - Reading from state
    - Conditional logic based on state values
    - Returning partial updates (only subject field)

    LangGraph Pattern:
    - Input: Complete EmailState
    - Output: Partial state update with only modified fields
    - Pure function: Same input always produces same output

    Args:
        state: Current email state

    Returns:
        Dictionary with updated subject field
    """
    email_type = state.get("email_type", "other")
    subject = state.get("subject", "")

    # Skip if subject is empty
    if not subject:
        return {}

    # Format based on email type
    if email_type == "business":
        formatted = f"[BUSINESS] {subject}"
    elif email_type == "support":
        formatted = f"[TICKET] {subject}"
    elif email_type == "personal":
        formatted = f"Personal: {subject}"
    else:
        formatted = subject

    # Return only the field we modified
    return {"subject": formatted}


def add_greeting_node(state: EmailState) -> dict[str, Any]:
    """
    Add a personalized greeting to the email body.

    This node demonstrates:
    - Building content based on state
    - String manipulation
    - Preserving existing content

    LangGraph Pattern:
    - Nodes should be composable
    - Each node does one thing well
    - Maintains immutability

    Args:
        state: Current email state

    Returns:
        Dictionary with updated body field
    """
    recipient = state.get("recipient", "")
    body = state.get("body", "")
    email_type = state.get("email_type", "other")

    # Extract name from email if possible
    if recipient and "@" in recipient:
        name = recipient.split("@")[0].replace(".", " ").title()
    else:
        name = "there"

    # Choose greeting based on email type
    if email_type == "business":
        greeting = f"Dear {name},\n\n"
    elif email_type == "support":
        greeting = f"Hello {name},\n\nThank you for contacting support.\n\n"
    elif email_type == "personal":
        greeting = f"Hi {name}!\n\n"
    else:
        greeting = f"Hello {name},\n\n"

    # Prepend greeting to body
    updated_body = greeting + body

    return {"body": updated_body}


def add_signature_node(state: EmailState) -> dict[str, Any]:
    """
    Add a signature to the email body.

    This node demonstrates:
    - Appending content to existing state
    - Using metadata to customize behavior
    - Time-based content generation

    LangGraph Pattern:
    - Nodes can use any field from state
    - Metadata field allows for extensibility
    - Keep transformations simple and focused

    Args:
        state: Current email state

    Returns:
        Dictionary with updated body field
    """
    body = state.get("body", "")
    email_type = state.get("email_type", "other")
    metadata = state.get("metadata", {})

    # Get sender name from metadata or use default
    sender_name = (
        metadata.get("sender_name", "Email Assistant")
        if metadata
        else "Email Assistant"
    )

    # Create signature based on email type
    if email_type == "business":
        signature = (
            f"\n\nBest regards,\n{sender_name}\n{datetime.now().strftime('%Y-%m-%d')}"
        )
    elif email_type == "support":
        signature = f"\n\nSincerely,\n{sender_name}\nSupport Team"
    elif email_type == "personal":
        signature = f"\n\nCheers,\n{sender_name}"
    else:
        signature = f"\n\nRegards,\n{sender_name}"

    # Append signature to body
    updated_body = body + signature

    return {"body": updated_body}


def validate_email_node(state: EmailState) -> dict[str, Any]:
    """
    Validate email fields and add validation metadata.

    This node demonstrates:
    - State validation
    - Adding metadata about processing
    - Error handling patterns

    LangGraph Pattern:
    - Nodes can validate and enrich state
    - Metadata is useful for tracking processing
    - Nodes should handle edge cases gracefully

    Args:
        state: Current email state

    Returns:
        Dictionary with updated metadata field
    """
    validation_results: dict[str, Any] = {
        "validated_at": datetime.now().isoformat(),
        "validation_passed": True,
        "issues": [],
    }
    issues: list[str] = []

    # Check required fields
    if not state.get("recipient"):
        validation_results["validation_passed"] = False
        issues.append("Missing recipient")
    elif "@" not in state.get("recipient", ""):
        validation_results["validation_passed"] = False
        issues.append("Invalid recipient email format")

    if not state.get("subject"):
        issues.append("Missing subject")

    if not state.get("body"):
        issues.append("Missing body")

    # Check for reasonable lengths
    subject = state.get("subject", "")
    if len(subject) > 200:
        issues.append("Subject too long (>200 chars)")

    body = state.get("body", "")
    if len(body) > 50000:
        issues.append("Body too long (>50000 chars)")

    validation_results["issues"] = issues

    # Merge with existing metadata
    current_metadata = state.get("metadata", {}) or {}
    updated_metadata = {
        **current_metadata,
        "validation": validation_results,
    }

    return {"metadata": updated_metadata}


def uppercase_subject_node(state: EmailState) -> dict[str, Any]:
    """
    Convert email subject to uppercase.

    This is a simple demonstration node showing:
    - Minimal transformation
    - Single responsibility
    - Easy testability

    Args:
        state: Current email state

    Returns:
        Dictionary with uppercase subject
    """
    subject = state.get("subject", "")
    if subject:
        return {"subject": subject.upper()}
    return {}


def word_count_node(state: EmailState) -> dict[str, Any]:
    """
    Add word count statistics to metadata.

    This node demonstrates:
    - Analyzing state without modifying core fields
    - Enriching metadata with computed values
    - Read-only operations on state

    Args:
        state: Current email state

    Returns:
        Dictionary with updated metadata containing word counts
    """
    subject = state.get("subject", "")
    body = state.get("body", "")

    # Calculate word counts
    subject_words = len(subject.split()) if subject else 0
    body_words = len(body.split()) if body else 0

    # Add statistics to metadata
    current_metadata = state.get("metadata", {}) or {}
    updated_metadata = {
        **current_metadata,
        "statistics": {
            "subject_word_count": subject_words,
            "body_word_count": body_words,
            "total_word_count": subject_words + body_words,
            "calculated_at": datetime.now().isoformat(),
        },
    }

    return {"metadata": updated_metadata}
