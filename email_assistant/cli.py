"""CLI entry point for Email Assistant."""

import typer
from rich.console import Console

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


if __name__ == "__main__":
    app()
