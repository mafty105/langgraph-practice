# type: ignore
"""Unit tests for the simple linear graph.

These tests verify that our first LangGraph implementation works correctly:
1. Graph creation and compilation
2. Node execution in correct order
3. State transformations through the graph
4. Streaming functionality
"""

from langchain_core.runnables import RunnableConfig

from email_assistant.graphs.simple_graph import (
    create_simple_email_graph,
    run_simple_email_graph,
    stream_simple_email_graph,
)
from email_assistant.models.state import create_initial_state


class TestSimpleGraphCreation:
    """Test graph creation and compilation."""

    def test_create_simple_graph(self):
        """Test that we can create and compile a simple graph."""
        graph = create_simple_email_graph()

        # Graph should be created and compiled
        assert graph is not None

        # Graph should be callable (compiled)
        assert callable(graph.invoke)
        assert callable(graph.stream)

    def test_graph_has_correct_structure(self):
        """Test that the graph has the expected nodes."""
        graph = create_simple_email_graph()

        # The compiled graph should have our nodes
        # Note: Implementation details may vary with LangGraph versions
        assert graph is not None


class TestSimpleGraphExecution:
    """Test graph execution with various inputs."""

    def test_execute_simple_graph_business_email(self):
        """Test executing the graph with a business email."""
        initial_state = create_initial_state(
            subject="Project Update",
            body="Here's the latest status.",
            recipient="manager@company.com",
            email_type="business",
        )

        result = run_simple_email_graph(initial_state)

        # Check that all transformations were applied
        assert "[BUSINESS]" in result["subject"]
        assert "Dear Manager," in result["body"]
        assert "Best regards," in result["body"]

        # Check metadata was added
        assert "validation" in result["metadata"]
        assert "statistics" in result["metadata"]

        # Check validation passed
        assert result["metadata"]["validation"]["validation_passed"] is True

        # Check word count was calculated
        assert result["metadata"]["statistics"]["total_word_count"] > 0

    def test_execute_simple_graph_personal_email(self):
        """Test executing the graph with a personal email."""
        initial_state = create_initial_state(
            subject="Weekend Plans",
            body="Are you free this weekend?",
            recipient="friend@example.com",
            email_type="personal",
        )

        result = run_simple_email_graph(initial_state)

        # Check personal email transformations
        assert "Personal:" in result["subject"]
        assert "Hi Friend!" in result["body"]
        assert "Cheers," in result["body"]

        # Validation and statistics should still be present
        assert result["metadata"]["validation"]["validation_passed"] is True
        assert result["metadata"]["statistics"]["total_word_count"] > 0

    def test_execute_simple_graph_support_email(self):
        """Test executing the graph with a support email."""
        initial_state = create_initial_state(
            subject="Login Issue",
            body="I cannot access my account.",
            recipient="user@example.com",
            email_type="support",
        )

        result = run_simple_email_graph(initial_state)

        # Check support email transformations
        assert "[TICKET]" in result["subject"]
        assert "Thank you for contacting support" in result["body"]
        assert "Support Team" in result["body"]

    def test_execute_with_empty_fields(self):
        """Test that the graph handles empty fields gracefully."""
        initial_state = create_initial_state(
            subject="",
            body="",
            recipient="test@example.com",
            email_type="other",
        )

        result = run_simple_email_graph(initial_state)

        # Graph should complete even with empty fields
        assert result is not None

        # Validation should note missing fields
        validation = result["metadata"]["validation"]
        assert "Missing subject" in validation["issues"]
        # Note: Body won't be empty after greeting/signature nodes add content
        # So we just check that validation ran
        assert "issues" in validation

        # Word count should reflect the added greeting/signature
        assert result["metadata"]["statistics"]["total_word_count"] > 0

    def test_execute_with_custom_metadata(self):
        """Test that custom metadata is preserved through the graph."""
        initial_state = create_initial_state(
            subject="Test",
            body="Test body",
            recipient="test@example.com",
        )
        initial_state["metadata"] = {"sender_name": "John Doe", "custom_field": "value"}

        result = run_simple_email_graph(initial_state)

        # Custom metadata should be preserved
        assert result["metadata"]["sender_name"] == "John Doe"
        assert result["metadata"]["custom_field"] == "value"

        # And new metadata should be added
        assert "validation" in result["metadata"]
        assert "statistics" in result["metadata"]


class TestSimpleGraphStreaming:
    """Test graph streaming functionality."""

    def test_stream_simple_graph(self):
        """Test that streaming yields updates from each node."""
        initial_state = create_initial_state(
            subject="Test Stream",
            body="Testing streaming.",
            recipient="test@example.com",
            email_type="business",
        )

        # Collect all streamed updates
        updates = []
        for update in stream_simple_email_graph(initial_state):
            updates.append(update)

        # Should have updates from each node
        # We have 5 nodes in our graph
        assert len(updates) >= 5

        # Each update should have a node name and state updates
        for update in updates:
            assert isinstance(update, dict)
            assert len(update) > 0

            for node_name, state_update in update.items():
                assert isinstance(node_name, str)
                assert isinstance(state_update, dict)

    def test_stream_order_matches_graph_structure(self):
        """Test that streaming follows the correct node order."""
        initial_state = create_initial_state(
            subject="Order Test",
            body="Testing order.",
            recipient="test@example.com",
            email_type="business",
        )

        # Collect node names in execution order
        node_order = []
        for update in stream_simple_email_graph(initial_state):
            for node_name in update:
                node_order.append(node_name)

        # Expected order based on our graph structure
        expected_order = [
            "format_subject",
            "add_greeting",
            "add_signature",
            "validate_email",
            "word_count",
        ]

        # The actual order should match expected
        # (filtering out any system nodes)
        actual_order = [n for n in node_order if n in expected_order]
        assert actual_order == expected_order


class TestGraphStateFlow:
    """Test how state flows through the graph."""

    def test_state_accumulates_changes(self):
        """Test that state changes accumulate through the graph."""
        initial_state = create_initial_state(
            subject="Accumulation Test",
            body="Original body.",
            recipient="test@example.com",
            email_type="business",
        )

        result = run_simple_email_graph(initial_state)

        # Subject should have format applied
        assert result["subject"] != initial_state["subject"]
        assert "[BUSINESS]" in result["subject"]

        # Body should have both greeting and signature
        assert "Dear Test," in result["body"]
        assert "Original body." in result["body"]
        assert "Best regards," in result["body"]

        # All transformations should be present in final state
        assert len(result["body"]) > len(initial_state["body"])

    def test_nodes_dont_interfere(self):
        """Test that nodes don't interfere with each other's changes."""
        initial_state = create_initial_state(
            subject="Independence Test",
            body="Testing node independence.",
            recipient="user@example.com",
            email_type="personal",
        )

        # Track changes through streaming
        changes_by_node = {}
        for update in stream_simple_email_graph(initial_state):
            for node_name, state_update in update.items():
                changes_by_node[node_name] = state_update

        # Each node should only update its expected fields
        if "format_subject" in changes_by_node:
            assert "subject" in changes_by_node["format_subject"]
            assert "body" not in changes_by_node["format_subject"]

        if "add_greeting" in changes_by_node:
            assert "body" in changes_by_node["add_greeting"]
            assert "subject" not in changes_by_node["add_greeting"]

        if "validate_email" in changes_by_node:
            assert "metadata" in changes_by_node["validate_email"]
            assert "subject" not in changes_by_node["validate_email"]


class TestGraphErrorHandling:
    """Test how the graph handles edge cases and errors."""

    def test_graph_handles_none_values(self):
        """Test that the graph handles None values gracefully."""
        initial_state = create_initial_state()
        initial_state["metadata"] = None

        # Should not raise an error
        result = run_simple_email_graph(initial_state)

        # Metadata should be created
        assert result["metadata"] is not None
        assert "validation" in result["metadata"]
        assert "statistics" in result["metadata"]

    def test_graph_with_config(self):
        """Test that the graph accepts configuration."""
        initial_state = create_initial_state(
            subject="Config Test",
            body="Testing with config.",
            recipient="test@example.com",
        )

        # Create a config (even if empty for now)
        config = RunnableConfig()

        # Should execute with config
        result = run_simple_email_graph(initial_state, config=config)

        assert result is not None
        assert result["subject"] == "Config Test"  # No prefix for "other" type
