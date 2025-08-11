# GitHub PR Workflow Preferences

## Single PR Policy

**IMPORTANT**: All related work should be combined into a single PR, even if the implementation is broken down into multiple logical steps.

### Why Single PR?
- Easier review process - all related changes in one place
- Better context - reviewers see the complete picture
- Simpler history - one merge commit for the feature
- Reduced CI/CD runs - tests run once for all changes

### How This Works

When working on multi-step tasks:
1. Create ONE feature branch at the start
2. Make all commits to that single branch
3. Push updates to the same PR as work progresses
4. The PR description can be updated to reflect completed steps

### Example Workflow

```bash
# Start of work - create ONE branch
git checkout -b feature/email-assistant-implementation

# Step 1: Basic CLI
git add <files>
git commit -m "Step 1: Add basic CLI structure"
git push

# Step 2: State management (SAME BRANCH)
git add <files>
git commit -m "Step 2: Add state management"
git push

# Step 3: LangGraph nodes (SAME BRANCH)
git add <files>
git commit -m "Step 3: Implement LangGraph nodes"
git push

# ONE PR for all steps
gh pr create --title "Complete Email Assistant Implementation"
```

### What NOT to Do

❌ Don't create separate branches for each step
❌ Don't create multiple PRs for related work
❌ Don't merge partial implementations to main

### Notes for Claude Code

When I ask you to implement something with multiple steps:
- Keep using the same branch throughout
- Make incremental commits but push to the same PR
- Update the PR description as you complete steps
- Only create a new PR if working on completely unrelated features

## Critical Git Rules

### NEVER Do These
1. **NEVER commit directly to main** - Always use feature branches
2. **NEVER merge PRs** - The user always handles merging
3. **NEVER reuse branch names** - Each branch should be unique
4. **NEVER leave branches after merge** - Clean up immediately

### ALWAYS Do These
1. **ALWAYS create a feature branch** for any changes
2. **ALWAYS use descriptive branch names** (feature/, fix/, docs/, etc.)
3. **ALWAYS delete branches after they're merged**
4. **ALWAYS close duplicate PRs immediately**
5. **ALWAYS wait for user to merge PRs**

## Branch Naming Convention

Use prefixes to indicate the type of change:
- `feature/` - New features or enhancements
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or updates
- `chore/` - Maintenance tasks

Example: `feature/add-email-parser`, `fix/memory-leak`, `docs/update-readme`
