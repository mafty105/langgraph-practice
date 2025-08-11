#!/bin/bash
# Hook to enforce step-by-step implementation from learning guide

# Read the JSON input from stdin
INPUT=$(cat)

# Extract tool name and file path if applicable
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.params.file_path // empty')
COMMAND=$(echo "$INPUT" | jq -r '.params.command // empty')

# Check current step from learning document
if [[ -f "$CLAUDE_PROJECT_DIR/docs/learning-langgraph-step-by-step.md" ]]; then
    CURRENT_STEP=$(grep -m1 "Current Step:" "$CLAUDE_PROJECT_DIR/docs/learning-langgraph-step-by-step.md" | sed 's/.*Current Step: //')

    # Provide context about current step
    if [[ -n "$CURRENT_STEP" ]]; then
        echo "[LEARNING GUIDE] Currently on: $CURRENT_STEP" >&2
        echo "[REMINDER] Follow the step-by-step guide in docs/learning-langgraph-step-by-step.md" >&2
    fi
fi

# Check if editing core files before basics are done
if [[ "$TOOL_NAME" == "Edit" || "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "MultiEdit" ]]; then
    if [[ "$FILE_PATH" == *"email_assistant/core/"* || "$FILE_PATH" == *"email_assistant/graphs/"* ]]; then
        if [[ "$CURRENT_STEP" == "Not started"* || "$CURRENT_STEP" == "Step 1"* ]]; then
            echo "[STEP WARNING] You're editing advanced components (core/graphs) but still on: $CURRENT_STEP" >&2
            echo "[SUGGESTION] Complete earlier steps first according to the learning guide" >&2
        fi
    fi
fi

# Remind about incremental implementation
if [[ "$TOOL_NAME" == "Write" ]]; then
    if [[ "$FILE_PATH" == *"email_assistant/"*.py ]]; then
        echo "[IMPLEMENTATION REMINDER] Keep implementations minimal for each step" >&2
        echo "[BEST PRACTICE] Add comprehensive docstrings explaining LangGraph concepts" >&2
    fi
fi

# Check if running tests
if [[ "$TOOL_NAME" == "Bash" && "$COMMAND" == *"pytest"* ]]; then
    echo "[TESTING REMINDER] Each step should be fully tested before moving on" >&2
fi

# Remind about updating progress
if [[ "$TOOL_NAME" == "Edit" || "$TOOL_NAME" == "Write" ]]; then
    echo "[PROGRESS REMINDER] Remember to update 'Current Step' in the learning guide after completing each step" >&2
fi

# Always allow the operation (exit 0)
exit 0
