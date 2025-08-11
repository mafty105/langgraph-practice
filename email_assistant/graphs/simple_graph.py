# type: ignore
"""Simple linear graph implementation using LangGraph.

This module demonstrates the fundamental concepts of LangGraph:
1. Creating a StateGraph with typed state
2. Adding nodes to the graph
3. Connecting nodes with edges in a linear sequence
4. Compiling the graph for execution

This is our first real LangGraph implementation!
"""

from typing import Any

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph

from email_assistant.models.state import EmailState
from email_assistant.nodes.email_processors import (
    add_greeting_node,
    add_signature_node,
    format_subject_node,
    validate_email_node,
    word_count_node,
)


def create_simple_email_graph() -> StateGraph:
    """
    Create a simple linear graph for email processing.

    This graph demonstrates the basic LangGraph pattern:
    - Linear flow from START to END
    - Each node transforms the state
    - State flows through each node in sequence

    Graph structure:
    START -> format_subject -> add_greeting -> add_signature
          -> validate -> word_count -> END

    LangGraph Concepts:
    1. StateGraph: Manages state flow through the graph
    2. add_node: Registers a node function with the graph
    3. add_edge: Creates directed connections between nodes
    4. START/END: Special nodes marking graph boundaries
    5. compile: Converts graph definition to executable form

    Returns:
        Compiled StateGraph ready for execution
    """
    # Create a StateGraph with our EmailState type
    # This tells LangGraph what type of state flows through our graph
    graph = StateGraph(EmailState)

    # Add nodes to the graph
    # Each node is a function that takes state and returns state updates
    # The first argument is the node name (used for edges and debugging)
    # The second argument is the actual node function

    print("Building LangGraph: Adding nodes...")

    graph.add_node("format_subject", format_subject_node)
    graph.add_node("add_greeting", add_greeting_node)
    graph.add_node("add_signature", add_signature_node)
    graph.add_node("validate_email", validate_email_node)
    graph.add_node("word_count", word_count_node)

    # Create edges to connect nodes in sequence
    # Edges define the flow of execution through the graph
    # START is a special node that marks the entry point

    print("Building LangGraph: Connecting nodes with edges...")

    # Connect START to the first node
    graph.add_edge(START, "format_subject")

    # Connect nodes in sequence
    graph.add_edge("format_subject", "add_greeting")
    graph.add_edge("add_greeting", "add_signature")
    graph.add_edge("add_signature", "validate_email")
    graph.add_edge("validate_email", "word_count")

    # Connect the last node to END
    # END is a special node that marks the exit point
    graph.add_edge("word_count", END)

    print("Building LangGraph: Compiling graph...")

    # Compile the graph
    # This converts our graph definition into an executable form
    # After compilation, the graph can process state
    compiled_graph = graph.compile()

    print("LangGraph compiled successfully!")

    return compiled_graph


def run_simple_email_graph(
    initial_state: EmailState,
    config: RunnableConfig | None = None,
) -> dict[str, Any]:
    """
    Execute the simple email graph with given initial state.

    This function demonstrates how to:
    1. Create a compiled graph
    2. Execute it with initial state
    3. Get the final transformed state

    LangGraph Execution:
    - The graph processes state through each node in sequence
    - Each node can read the full state
    - Each node returns partial updates
    - LangGraph merges updates into the state
    - Final state contains all transformations

    Args:
        initial_state: The starting EmailState
        config: Optional configuration for execution

    Returns:
        Final state after all transformations
    """
    # Create and compile the graph
    graph = create_simple_email_graph()

    # Execute the graph with initial state
    # The invoke method runs the graph from START to END
    # It returns the final state after all nodes have processed
    print("\nExecuting LangGraph...")
    print(f"Initial state: {initial_state.get('subject', 'No subject')}")

    result = graph.invoke(initial_state, config=config)

    print(f"Final state: {result.get('subject', 'No subject')}")
    print("LangGraph execution complete!\n")

    return result  # type: ignore


def stream_simple_email_graph(
    initial_state: EmailState,
    config: RunnableConfig | None = None,
):
    """
    Stream the execution of the simple email graph.

    This demonstrates LangGraph's streaming capability:
    - See state changes at each node
    - Useful for debugging and visualization
    - Shows the step-by-step transformation

    LangGraph Streaming:
    - stream() yields updates as they happen
    - Each yield shows which node ran and what it changed
    - Helps understand graph execution flow

    Args:
        initial_state: The starting EmailState
        config: Optional configuration for execution

    Yields:
        State updates from each node
    """
    # Create and compile the graph
    graph = create_simple_email_graph()

    print("\nStreaming LangGraph execution...")
    print("=" * 50)

    # Stream the execution
    # This yields results as each node completes
    for update in graph.stream(initial_state, config=config):
        # Each update is a dict with node name as key
        # and state updates as value
        for node_name, state_update in update.items():
            print(f"\nNode: {node_name}")
            print(f"Updates: {state_update}")
            print("-" * 30)

        # Yield the update for the caller
        yield update

    print("=" * 50)
    print("Streaming complete!\n")


def get_graph_structure() -> dict[str, Any]:
    """
    Get the structure of the simple email graph.

    This is useful for understanding and visualizing the graph.

    Returns:
        Dictionary describing the graph structure
    """
    graph = create_simple_email_graph()

    # Get graph structure
    # This includes nodes, edges, and other metadata
    structure = {
        "nodes": list(graph.nodes.keys()) if hasattr(graph, "nodes") else [],
        "edges": [],  # Would need to extract from graph internals
        "description": "Linear email processing graph",
    }

    return structure
