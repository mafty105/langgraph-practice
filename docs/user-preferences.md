# User Preferences and Rules for Claude Code

This document contains all the specific preferences and rules that have been communicated by the user for this project.

## Git Workflow Rules

### Branch Management
1. **ALWAYS create feature branches** - Never work directly on main
2. **NEVER commit directly to main** - This is strictly forbidden
3. **Use descriptive branch names** - e.g., `feature/add-auth`, `docs/update-readme`, `fix/memory-leak`
4. **Delete branches after merge** - Clean up both local and remote branches
5. **Never reuse branch names** - Each branch name should be unique

### Pull Request Rules
1. **ONE PR per feature/task** - Even if the implementation has multiple steps
2. **NEVER merge PRs** - The user always handles merging
3. **All related work goes in the same PR** - Don't split related changes across multiple PRs
4. **Update existing PRs** - Add commits to the same branch/PR for related work
5. **Close duplicate PRs immediately** - If accidentally created

### What NOT to Do
❌ **Don't commit directly to main** - "it's too idiot" as the user said
❌ **Don't merge PRs** - Ever. The user handles all merges
❌ **Don't create multiple PRs for related work**
❌ **Don't create new branches for each step of a multi-step task**

## Development Approach

### Step-by-Step Implementation
1. **Follow the learning guide** - Refer to `docs/learning-langgraph-step-by-step.md`
2. **Complete steps sequentially** - Don't skip ahead to advanced features
3. **Keep implementations minimal** - Only implement what's needed for each step
4. **Test each step thoroughly** - Before moving to the next step
5. **Update progress tracking** - Mark current step in the learning guide

### Documentation Requirements
1. **Add comprehensive docstrings** - Explain LangGraph concepts in detail
2. **Include inline comments** - For learning points and important concepts
3. **Update progress in learning guide** - After completing each step

## Claude Code Hooks Configuration

### Configured Hooks
1. **Single PR Enforcement** - Reminds about single PR preference
2. **Step-by-Step Enforcement** - Ensures following the learning guide
3. **Workflow Reminders** - Adds context about user preferences to every interaction

### Hook Behavior
- Hooks provide **reminders, not blocks** - They won't prevent operations
- Hooks run on relevant git commands and file edits
- Local settings in `.claude/settings.local.json` (not committed to git)

## Project-Specific Preferences

### Testing
- Run tests with `pytest` after each implementation
- Ensure all tests pass before considering a step complete
- Each step should have corresponding tests

### Code Quality
- Run `ruff format .` and `ruff check .` before committing
- Run `mypy email_assistant` for type checking
- Pre-commit hooks will auto-format and check code

### Communication Style
- Be concise and direct
- No unnecessary explanations unless asked
- Follow instructions exactly - "do what has been asked; nothing more, nothing less"

## Important Reminders

1. **This is a learning project** - Understanding is more important than features
2. **Single PR for all related work** - Even multi-step implementations
3. **Never merge PRs** - This is the user's responsibility
4. **Follow the documented steps** - Don't skip ahead in the learning guide
5. **Clean up after merges** - Delete feature branches promptly

## User's Direct Quotes

- On committing to main: "why didn't you make a new branch? are you crazy? if you know Git. it's too idiot"
- On PR workflow: "I want it to be 1PR even if the plan seems to be broken down into smaller parts"
- On merging: "No you shouldn't merge it. I always merge branches by myself"

---

*This document should be treated as the authoritative source for user preferences in this project.*
