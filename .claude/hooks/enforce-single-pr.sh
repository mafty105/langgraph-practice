#!/bin/bash
# Hook to remind about single PR workflow preference

# Read the JSON input from stdin
INPUT=$(cat)

# Extract tool name and parameters
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
TOOL_PARAMS=$(echo "$INPUT" | jq -r '.params.command // empty')

# Check if trying to create a new branch when one already exists
if [[ "$TOOL_NAME" == "Bash" ]]; then
    if [[ "$TOOL_PARAMS" == *"git checkout -b"* ]] || [[ "$TOOL_PARAMS" == *"git switch -c"* ]]; then
        CURRENT_BRANCH=$(git branch --show-current 2>/dev/null)
        if [[ "$CURRENT_BRANCH" != "main" ]] && [[ "$CURRENT_BRANCH" != "master" ]]; then
            echo "[WORKFLOW REMINDER] Current branch: '$CURRENT_BRANCH'. User prefers single PR - consider using existing branch for related work." >&2
        fi
    fi

    # Check if trying to create multiple PRs
    if [[ "$TOOL_PARAMS" == *"gh pr create"* ]]; then
        EXISTING_PR=$(gh pr list --author @me --state open --json number --jq '.[0].number' 2>/dev/null)
        if [[ -n "$EXISTING_PR" ]]; then
            echo "[WORKFLOW REMINDER] Open PR #$EXISTING_PR exists. User prefers single PR for all related work, even multi-step implementations." >&2
        fi
    fi
fi

# Always allow the operation (exit 0), just provide reminders
exit 0
