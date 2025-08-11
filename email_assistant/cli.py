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


if __name__ == "__main__":
    app()
