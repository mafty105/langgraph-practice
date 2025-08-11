"""State definitions for LangGraph email assistant.

This module defines the state structure used throughout the LangGraph workflow.
In LangGraph, state is the central concept that flows through all nodes in a graph.

Key LangGraph Concepts:
1. State is defined using TypedDict for type safety
2. State is immutable - nodes return new state, not modify existing
3. Each field in state can be updated independently by different nodes
4. State acts as the communication mechanism between nodes
"""

from datetime import datetime
from typing import Any, Literal, TypedDict


class EmailState(TypedDict):
    """
    The central state object for the email assistant workflow.

    In LangGraph, this TypedDict defines the structure of data that flows
    through the graph. Each node in the graph receives this state as input
    and returns a modified version as output.

    LangGraph State Principles:
    - State should contain all data needed by any node in the graph
    - Fields can be optional if not all nodes need them
    - State is the single source of truth during graph execution
    - Nodes should return only the fields they modify (partial updates)

    Attributes:
        subject: The email subject line
        body: The main content of the email
        recipient: Email address of the recipient
        email_type: Category of email (business, personal, support, other)
        created_at: Timestamp when the state was first created
        modified_at: Timestamp of the last modification
        metadata: Additional flexible data storage
    """

    subject: str
    body: str
    recipient: str
    email_type: Literal["business", "personal", "support", "other"]
    created_at: datetime | None
    modified_at: datetime | None
    metadata: dict[str, Any] | None


def create_initial_state(
    subject: str = "",
    body: str = "",
    recipient: str = "",
    email_type: Literal["business", "personal", "support", "other"] = "other",
) -> EmailState:
    """
    Create an initial EmailState with default values.

    This is a helper function that demonstrates how to create state objects
    in LangGraph. In practice, initial state is often created from user input
    or external data sources.

    LangGraph Pattern:
    - Initial state creation happens before graph execution
    - All required fields must be provided
    - Optional fields can be None initially and populated by nodes

    Args:
        subject: Email subject line
        body: Email body content
        recipient: Recipient email address
        email_type: Type of email

    Returns:
        A new EmailState instance with timestamps set
    """
    now = datetime.now()
    return EmailState(
        subject=subject,
        body=body,
        recipient=recipient,
        email_type=email_type,
        created_at=now,
        modified_at=now,
        metadata={},
    )


def update_state(state: EmailState, **updates: Any) -> EmailState:
    """
    Create a new state with updates applied.

    This helper demonstrates the immutability principle in LangGraph.
    Instead of modifying state in-place, we create a new state object
    with the updates applied.

    LangGraph Pattern:
    - Nodes should not modify state directly
    - Always return a new state object
    - Use dictionary unpacking for partial updates
    - Update modified_at when state changes

    Args:
        state: Current state
        **updates: Fields to update

    Returns:
        New EmailState with updates applied
    """
    new_state: dict[str, Any] = dict(state)
    new_state.update(updates)
    if updates:
        new_state["modified_at"] = datetime.now()
    return EmailState(
        subject=new_state["subject"],
        body=new_state["body"],
        recipient=new_state["recipient"],
        email_type=new_state["email_type"],
        created_at=new_state.get("created_at"),
        modified_at=new_state.get("modified_at"),
        metadata=new_state.get("metadata"),
    )


def format_state_display(state: EmailState) -> str:
    """
    Format state for display purposes.

    This is useful for debugging and demonstrating state contents
    during development and learning.

    Args:
        state: The state to format

    Returns:
        Formatted string representation of the state
    """
    lines = [
        "=" * 50,
        "EmailState Contents:",
        "=" * 50,
        f"Subject: {state['subject'] or '(empty)'}",
        f"Recipient: {state['recipient'] or '(empty)'}",
        f"Email Type: {state['email_type']}",
        f"Body: {state['body'] or '(empty)'}",
        "-" * 50,
    ]

    created_at = state.get("created_at")
    if created_at:
        lines.append(f"Created: {created_at.isoformat()}")
    modified_at = state.get("modified_at")
    if modified_at:
        lines.append(f"Modified: {modified_at.isoformat()}")

    if state.get("metadata"):
        lines.append(f"Metadata: {state['metadata']}")

    lines.append("=" * 50)
    return "\n".join(lines)
