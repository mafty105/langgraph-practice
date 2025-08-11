# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Email Assistant CLI application built with LangGraph, designed as a learning project to understand LangGraph concepts step-by-step.

## Important Context

### Learning Approach
- **CRITICAL**: This project is being built incrementally for learning purposes
- **Follow the guide**: Always refer to `docs/learning-langgraph-step-by-step.md`
- **Small steps**: Make minimal changes at each step
- **Test everything**: Each step should be fully tested before moving on

### Current Progress
- **Current Step**: Not started (ready to begin Step 1)
- **Environment**: Python 3.11 with LangGraph 0.6.4 installed

### User Preferences (MUST FOLLOW)
- **Git Workflow**: See `WORKFLOW.md` and `USER_PREFERENCES.md` for detailed rules
- **Single PR Policy**: All related work in ONE PR, even multi-step implementations
- **NEVER merge PRs**: User always handles merging
- **NEVER commit to main**: Always use feature branches
- **Branch cleanup**: Delete branches after merge

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
source .venv/bin/activate

# Install/update dependencies
uv sync --all-extras
```

### Running the Application
```bash
# Run CLI
python -m email_assistant.cli --help

# Run with specific command (after implementation)
python -m email_assistant.cli [command]
```

### Testing
```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/unit/test_cli.py -v

# Run with watch mode (if needed)
pytest-watch
```

### Code Quality
```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy email_assistant

# Run all checks
ruff format . && ruff check . && mypy email_assistant
```

## Project Structure

```
email_assistant/
├── __init__.py           # Package initialization
├── cli.py               # CLI entry point (Typer app)
├── core/                # Core business logic
│   ├── __init__.py
│   ├── state.py         # LangGraph state definitions
│   ├── nodes/           # LangGraph nodes
│   ├── graphs/          # LangGraph graph definitions
│   └── memory/          # Checkpointing and persistence
└── utils/               # Utility functions
```

## Development Guidelines

### When Implementing Each Step:

1. **Read the step description** in `docs/learning-langgraph-step-by-step.md`
2. **Implement only what's needed** for that specific step
3. **Add comprehensive docstrings** explaining LangGraph concepts
4. **Write tests first** (TDD approach)
5. **Update the progress** in the learning document

### Code Style Requirements:
- Use type hints for all functions
- Add docstrings with LangGraph concept explanations
- Keep functions small and focused
- Use descriptive variable names
- Add inline comments for learning points

### Example of Good Documentation:
```python
def my_node(state: EmailState) -> EmailState:
    """
    A LangGraph node that processes email state.

    In LangGraph, nodes are pure functions that:
    1. Take state as input
    2. Return modified state as output
    3. Should not have side effects

    Args:
        state: The current EmailState

    Returns:
        Modified EmailState with updated fields
    """
    # LangGraph concept: State is immutable, so we create a new dict
    return {**state, "processed": True}
```

## Important Reminders

1. **This is a learning project** - prioritize understanding over features
2. **Follow the step-by-step guide** - don't skip ahead
3. **Keep changes minimal** - each step should be a small, digestible change
4. **Test everything** - ensure each concept works before moving on
5. **Document learning points** - add comments explaining LangGraph concepts

## Common Patterns in This Project

### State Management
- Use TypedDict for state definitions
- Always return new state objects (immutability)
- Use Pydantic for validation when needed

### Node Creation
- Nodes are pure functions
- Input: state, Output: state
- No side effects in nodes

### Graph Construction
- Create StateGraph instance
- Add nodes with descriptive names
- Connect with edges or conditional edges
- Compile before execution

## Technology Stack Reference
- See `docs/technology-stack-documentation.md` for full stack details
- Key libraries: LangGraph, LangChain, Typer, Pydantic, Rich

## Questions or Issues?
- Check the learning guide first
- Ensure you're on the correct step
- Verify all previous steps are complete and tested
