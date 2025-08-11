"""Graphs package for Email Assistant.

This package contains LangGraph graph definitions - complete workflows
that connect nodes together to process emails.

LangGraph Graph Concepts:
- Graphs define the flow of data through nodes
- StateGraph manages state transitions between nodes
- Edges connect nodes in sequence or conditionally
- Compiled graphs can be executed with initial state
"""

from email_assistant.graphs.simple_graph import (
    create_simple_email_graph,  # type: ignore[attr-defined]
)

__all__ = ["create_simple_email_graph"]
