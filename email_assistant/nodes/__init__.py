"""Nodes package for Email Assistant.

This package contains LangGraph nodes - the fundamental processing units
that transform state in a graph workflow.

LangGraph Node Concepts:
- Nodes are pure functions that take state and return state
- Each node performs a specific transformation
- Nodes can be composed into graphs for complex workflows
"""

from email_assistant.nodes.email_processors import (
    add_greeting_node,
    add_signature_node,
    format_subject_node,
    validate_email_node,
)

__all__ = [
    "format_subject_node",
    "add_greeting_node",
    "add_signature_node",
    "validate_email_node",
]
