"""CLI entry point for Email Assistant."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from email_assistant.models.state import (
    create_initial_state,
    format_state_display,
    update_state,
)
from email_assistant.nodes import (
    add_greeting_node,
    add_signature_node,
    format_subject_node,
    validate_email_node,
)

app = typer.Typer(
    name="email-assistant",
    help="AI-powered email assistant CLI using LangGraph",
    add_completion=True,
)
console = Console()


@app.command()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit",
    ),
) -> None:
    """Email Assistant CLI - Intelligent email composition powered by AI."""
    if version:
        from email_assistant import __version__

        console.print(f"Email Assistant CLI v{__version__}")
        raise typer.Exit()

    console.print("[bold green]Welcome to Email Assistant CLI![/bold green]")
    console.print("Use --help to see available commands.")


@app.command()
def state_demo() -> None:
    """
    Demonstrate LangGraph state management concepts.

    This command shows how state works in LangGraph:
    1. Creating initial state
    2. Updating state immutably
    3. Displaying state contents

    This is Step 1 of our learning journey!
    """
    console.print("\n[bold cyan]LangGraph State Management Demo[/bold cyan]\n")
    console.print("This demo shows the fundamental concept of state in LangGraph.")
    console.print("State is the data that flows through your graph nodes.\n")

    console.print("[yellow]Step 1: Creating initial state...[/yellow]")
    initial_state = create_initial_state(
        subject="Welcome to LangGraph",
        body="This is a demo email to show state management.",
        recipient="demo@example.com",
        email_type="business",
    )

    console.print(
        Panel(
            format_state_display(initial_state),
            title="Initial State",
            border_style="green",
        )
    )

    console.print("\n[yellow]Step 2: Updating state immutably...[/yellow]")
    console.print("In LangGraph, we never modify state directly.")
    console.print("Instead, we create a new state with updates.\n")

    updated_state = update_state(
        initial_state,
        subject="Updated: Learning LangGraph State Management",
        body="The body has been updated to demonstrate immutability.",
    )

    console.print(
        Panel(
            format_state_display(updated_state),
            title="Updated State",
            border_style="blue",
        )
    )

    console.print("\n[yellow]Step 3: Demonstrating partial updates...[/yellow]")
    console.print("Nodes can update only specific fields they care about.\n")

    partial_update = update_state(
        updated_state,
        metadata={"processed_by": "state_demo", "step": 1},
    )

    console.print(
        Panel(
            format_state_display(partial_update),
            title="State with Metadata",
            border_style="magenta",
        )
    )

    console.print("\n[bold green]✓ State Demo Complete![/bold green]")
    console.print("\n[dim]Key Takeaways:[/dim]")

    table = Table(show_header=False, box=None)
    table.add_column(style="cyan", no_wrap=True)
    table.add_column()

    table.add_row("1.", "State is defined using TypedDict for type safety")
    table.add_row("2.", "State is immutable - always create new state objects")
    table.add_row("3.", "Nodes receive state as input and return updated state")
    table.add_row("4.", "Partial updates are common - nodes update only what they need")

    console.print(table)
    console.print()


@app.command()
def node_demo() -> None:
    """
    Demonstrate LangGraph node concepts.

    This command shows how nodes work in LangGraph:
    1. Nodes are pure functions (state in → state out)
    2. Nodes return partial updates
    3. Nodes can be composed sequentially
    4. Each node has a single responsibility

    This is Step 2 of our learning journey!
    """
    console.print("\n[bold cyan]LangGraph Node Processing Demo[/bold cyan]\n")
    console.print("This demo shows how nodes transform state in LangGraph.")
    console.print("Nodes are the building blocks of graph workflows.\n")

    # Create initial state
    console.print("[yellow]Creating initial email state...[/yellow]")
    state = create_initial_state(
        subject="Project Update",
        body="Here's the latest status on our project.",
        recipient="john.doe@example.com",
        email_type="business",
    )

    console.print(
        Panel(
            format_state_display(state),
            title="Initial State",
            border_style="dim",
        )
    )

    # Apply format_subject_node
    console.print("\n[yellow]Node 1: format_subject_node[/yellow]")
    console.print("This node adds a prefix based on email type.")

    subject_update = format_subject_node(state)
    console.print(f"Node returned: {subject_update}")
    state = update_state(state, **subject_update)

    console.print(
        Panel(
            format_state_display(state),
            title="After format_subject_node",
            border_style="green",
        )
    )

    # Apply add_greeting_node
    console.print("\n[yellow]Node 2: add_greeting_node[/yellow]")
    console.print("This node adds a personalized greeting to the body.")

    greeting_update = add_greeting_node(state)
    console.print(f"Node returned partial update with {len(greeting_update)} field(s)")
    state = update_state(state, **greeting_update)

    console.print(
        Panel(
            format_state_display(state),
            title="After add_greeting_node",
            border_style="blue",
        )
    )

    # Apply add_signature_node
    console.print("\n[yellow]Node 3: add_signature_node[/yellow]")
    console.print("This node adds a signature to the email.")

    # Add sender name to metadata for signature
    state = update_state(state, metadata={"sender_name": "Alice Smith"})
    signature_update = add_signature_node(state)
    state = update_state(state, **signature_update)

    console.print(
        Panel(
            format_state_display(state),
            title="After add_signature_node",
            border_style="magenta",
        )
    )

    # Apply validate_email_node
    console.print("\n[yellow]Node 4: validate_email_node[/yellow]")
    console.print("This node validates the email and adds metadata.")

    validation_update = validate_email_node(state)
    state = update_state(state, **validation_update)

    console.print(
        Panel(
            format_state_display(state),
            title="After validate_email_node",
            border_style="yellow",
        )
    )

    # Show key concepts
    console.print("\n[bold green]✓ Node Demo Complete![/bold green]")
    console.print("\n[dim]Key Node Concepts:[/dim]")

    table = Table(show_header=False, box=None)
    table.add_column(style="cyan", no_wrap=True)
    table.add_column()

    table.add_row("1.", "Nodes are pure functions - same input gives same output")
    table.add_row("2.", "Nodes return partial updates - only modified fields")
    table.add_row("3.", "Nodes compose sequentially - output feeds next input")
    table.add_row("4.", "Each node has single responsibility - do one thing well")
    table.add_row("5.", "Nodes maintain immutability - never modify input state")

    console.print(table)
    console.print(
        "\n[dim]Next: Step 3 will show how to connect nodes into a graph![/dim]\n"
    )


if __name__ == "__main__":
    app()
