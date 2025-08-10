# Pull Request Notes

This document tracks important notes for the initial setup PR.

## Setup Instructions

1. Clone the repository
2. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Create virtual environment: `uv venv`
4. Install dependencies: `uv sync --all-extras`
5. Activate environment: `source .venv/bin/activate`

## Next Steps

After this PR is merged, we'll begin implementing Step 1 from the learning guide:
- Basic CLI structure with Typer
- Simple state management
- First LangGraph node

## Testing

Run the following commands to verify the setup:
```bash
# Run tests
pytest

# Check CLI
python -m email_assistant.cli --version

# Run pre-commit checks
pre-commit run --all-files
```
