# Makefile for Email Assistant CLI
# Run 'make help' to see available commands

.PHONY: help
help: ## Show this help message
	@echo "Email Assistant CLI - Development Commands"
	@echo "=========================================="
	@echo ""
	@echo "Usage: make [command]"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Environment setup
.PHONY: install
install: ## Install dependencies with uv
	uv sync --all-extras

.PHONY: install-dev
install-dev: ## Install in editable mode for development
	pip install -e .

.PHONY: venv
venv: ## Create virtual environment (if not using uv)
	python -m venv .venv
	@echo "Run 'source .venv/bin/activate' to activate"

# CLI Commands
.PHONY: cli
cli: ## Show CLI help
	@if [ -d .venv ]; then \
		.venv/bin/python -m email_assistant.cli --help; \
	else \
		python -m email_assistant.cli --help; \
	fi

.PHONY: run
run: ## Run the main CLI command
	@if [ -d .venv ]; then \
		.venv/bin/python -m email_assistant.cli main; \
	else \
		python -m email_assistant.cli main; \
	fi

.PHONY: demo
demo: ## Run the state-demo command
	@if [ -d .venv ]; then \
		.venv/bin/python -m email_assistant.cli state-demo; \
	else \
		python -m email_assistant.cli state-demo; \
	fi

.PHONY: version
version: ## Show version
	@if [ -d .venv ]; then \
		.venv/bin/python -m email_assistant.cli main --version; \
	else \
		python -m email_assistant.cli main --version; \
	fi

# Testing
.PHONY: test
test: ## Run all tests with coverage
	@if [ -d .venv ]; then \
		.venv/bin/pytest; \
	else \
		pytest; \
	fi

.PHONY: test-verbose
test-verbose: ## Run tests with verbose output
	@if [ -d .venv ]; then \
		.venv/bin/pytest -xvs; \
	else \
		pytest -xvs; \
	fi

.PHONY: test-watch
test-watch: ## Run tests in watch mode (requires pytest-watch)
	@if [ -d .venv ]; then \
		.venv/bin/pytest-watch; \
	else \
		pytest-watch; \
	fi

.PHONY: test-unit
test-unit: ## Run only unit tests
	@if [ -d .venv ]; then \
		.venv/bin/pytest tests/unit -v; \
	else \
		pytest tests/unit -v; \
	fi

.PHONY: test-integration
test-integration: ## Run only integration tests
	@if [ -d .venv ]; then \
		.venv/bin/pytest tests/integration -v; \
	else \
		pytest tests/integration -v; \
	fi

.PHONY: coverage
coverage: ## Generate HTML coverage report
	@if [ -d .venv ]; then \
		.venv/bin/pytest --cov=email_assistant --cov-report=html; \
	else \
		pytest --cov=email_assistant --cov-report=html; \
	fi
	@echo "Coverage report generated in htmlcov/index.html"

# Code Quality
.PHONY: format
format: ## Format code with ruff
	@if [ -d .venv ]; then \
		.venv/bin/ruff format .; \
	else \
		ruff format .; \
	fi

.PHONY: lint
lint: ## Lint code with ruff
	@if [ -d .venv ]; then \
		.venv/bin/ruff check .; \
	else \
		ruff check .; \
	fi

.PHONY: lint-fix
lint-fix: ## Lint and auto-fix issues
	@if [ -d .venv ]; then \
		.venv/bin/ruff check . --fix; \
	else \
		ruff check . --fix; \
	fi

.PHONY: typecheck
typecheck: ## Type check with mypy
	@if [ -d .venv ]; then \
		.venv/bin/mypy email_assistant; \
	else \
		mypy email_assistant; \
	fi

.PHONY: check
check: format lint typecheck ## Run all code quality checks

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	pre-commit run --all-files

# Git Commands
.PHONY: status
status: ## Show git status
	git status

.PHONY: diff
diff: ## Show git diff
	git diff

.PHONY: branch
branch: ## Show current branch
	git branch --show-current

# Development Workflow
.PHONY: dev
dev: ## Run development server (for future use)
	@echo "Development server not yet implemented"
	@echo "Use 'make demo' to run the state demo"

.PHONY: clean
clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

.PHONY: clean-all
clean-all: clean ## Clean everything including virtual environment
	rm -rf .venv

# Quick commands for common workflows
.PHONY: ready
ready: install check test ## Get ready for development (install, check, test)

.PHONY: pr
pr: check test ## Prepare for PR (run checks and tests)
	@echo "✅ Ready for PR!"

.PHONY: merge-main
merge-main: ## Merge main into current branch
	git fetch origin main
	git merge origin/main

.PHONY: update
update: merge-main install ## Update branch and dependencies

# Default target
.DEFAULT_GOAL := help
