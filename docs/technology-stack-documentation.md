# Email Assistant CLI - Technology Stack Documentation

## Core Framework & Architecture

### LangGraph Framework
- **Version**: 0.2.x+
- **Purpose**: Primary framework for AI agent orchestration and workflow management
- **Justification**: Production-ready framework adopted by major companies (Uber, LinkedIn), provides low-level control over agent architecture, excellent state management, and built-in checkpoint capabilities

### Python Version Strategy
- **Target Version**: Python 3.11
- **Minimum Version**: Python 3.11
- **Rationale**: Optimal balance of modern features, performance improvements, and ecosystem compatibility

## Package Management & Build System

### Package Manager
- **Primary**: uv (Astral)
- **Version**: Latest stable
- **Benefits**: 10-100x faster than traditional tools, Rust-powered, combines functionality of pip/poetry/pyenv
- **Alternative**: Poetry 2.0 (if team already invested in Poetry ecosystem)

### Build System
- **Tool**: Hatchling
- **Configuration**: pyproject.toml (PEP 621 compliant)
- **Standards**: Modern Python packaging standards with optional dependencies

## Code Quality & Formatting

### Linter & Formatter
- **Tool**: Ruff
- **Version**: 0.7.x+
- **Capabilities**: Replaces Flake8, Black, isort, pyupgrade, autoflake in single tool
- **Performance**: 10-100x faster than traditional tools
- **Rules**: Comprehensive rule set including pycodestyle, pyflakes, bugbear, comprehensions

### Code Quality Features
- **Auto-fixing**: Automatic issue resolution where possible
- **Real-time feedback**: Sub-second execution for immediate feedback
- **Extensible configuration**: Customizable rules per file/directory

## Type Checking & Safety

### Type Checkers
- **Primary**: mypy
- **Version**: 1.15+
- **Configuration**: Strict mode enabled
- **Secondary**: Pyright (for VS Code integration via Pylance)

### Runtime Validation
- **Tool**: Pydantic v2
- **Version**: 2.9+
- **Purpose**: Runtime type validation, configuration management
- **Performance**: 4-50x faster than v1 due to Rust core

### Type Safety Strategy
- **Coverage**: 100% type annotation requirement
- **Strictness**: Strict mode for both mypy and Pyright
- **Integration**: Seamless integration between static and runtime type checking

## Testing Framework

### Core Testing
- **Framework**: pytest
- **Version**: 8.0+
- **Plugins**:
  - pytest-cov (coverage measurement)
  - pytest-asyncio (async support)
  - pytest-xdist (parallel testing)
  - Hypothesis (property-based testing)

### Coverage Requirements
- **Minimum**: 85% line coverage
- **Target**: 90%+ for critical modules
- **Branch coverage**: Enabled
- **Reporting**: HTML and terminal reports

### Testing Strategy
- **Unit tests**: Core logic and individual components
- **Integration tests**: LangGraph workflow testing
- **Property-based tests**: Agent behavior validation
- **Async testing**: Proper handling of async workflows

## CLI Framework

### CLI Library
- **Framework**: Typer
- **Version**: 0.12+
- **Features**: Type-hint based CLI generation, auto-completion, validation
- **Integration**: Seamless Pydantic integration for configuration

### Terminal UI
- **Tool**: Rich-click
- **Purpose**: Beautiful terminal output, progress bars, tables
- **Integration**: Enhanced Typer/Click output formatting

## Development Environment

### Pre-commit Hooks
- **Tool**: pre-commit
- **Version**: 3.8+
- **Hooks**:
  - Ruff (linting and formatting)
  - mypy (type checking)
  - Security scanning (Bandit)
  - Standard hooks (trailing whitespace, YAML/TOML validation)

### IDE Integration
- **Primary**: VS Code with extensions:
  - Pylance (Pyright integration)
  - Ruff extension
  - Python extension
- **Alternative**: PyCharm Professional (built-in Python support)

### Environment Management
- **Tool**: uv (handles Python versions and virtual environments)
- **Configuration**: pyproject.toml for dependency specification
- **Development dependencies**: Separate dev dependency groups

## CI/CD Pipeline

### Platform
- **Tool**: GitHub Actions
- **Justification**: Native Python support, extensive marketplace, excellent performance

### Pipeline Features
- **Matrix testing**: Multiple Python versions and OS
- **Parallel execution**: Simultaneous testing across environments
- **Security scanning**: Automated vulnerability detection
- **Coverage reporting**: Integration with Codecov
- **Dependency updates**: Automated via Renovate (preferred over Dependabot)

### Deployment Strategy
- **Containerization**: Docker multi-stage builds
- **Distribution**: PyPI packaging
- **Release automation**: Automated versioning and release

## Logging & Observability

### Logging Framework
- **Tool**: Loguru
- **Features**: Structured logging, automatic rotation, rich exception handling
- **Output**: JSON format for production, formatted for development

### Observability
- **Integration**: LangSmith for LangGraph tracing
- **Monitoring**: Application metrics and performance tracking
- **Error tracking**: Structured error reporting with context

## Documentation

### Documentation Generator
- **Tool**: MkDocs with Material theme
- **Plugin**: mkdocstrings for auto-generated API docs
- **Format**: Markdown-based documentation
- **Features**: Search, navigation, code highlighting, responsive design

### Documentation Strategy
- **User guides**: Step-by-step usage instructions
- **API reference**: Auto-generated from docstrings
- **Architecture**: System design and workflow documentation
- **Development**: Contributing guidelines and setup instructions

## Security & Dependencies

### Security Scanning
- **Static analysis**: Bandit for security issues
- **Dependency scanning**: pip-audit for vulnerability detection
- **Supply chain**: Dependency pinning and lock files

### Dependency Management
- **Strategy**: Minimal direct dependencies
- **Updates**: Automated via Renovate
- **Security**: Regular security updates and monitoring

## Language Processing (Japanese Support)

### Text Processing
- **Requirements**: Full-width/half-width character handling
- **Business context**: Japanese business email conventions
- **Keigo analysis**: Honorific language processing capabilities

### LLM Integration
- **Strategy**: English/Japanese thinking with Japanese output
- **Context**: Japanese business culture awareness
- **Validation**: Japanese text validation and formatting

## Performance Considerations

### Optimization Strategy
- **Cold start**: Minimized import time for CLI responsiveness
- **Memory usage**: Efficient state management for long-running processes
- **Concurrency**: Async support for I/O operations
- **Caching**: Strategic caching for expensive operations

### Monitoring
- **Performance metrics**: Response time and throughput monitoring
- **Resource usage**: Memory and CPU usage tracking
- **Scalability**: Load testing for high-volume usage

## Configuration Management

### Configuration Strategy
- **Format**: YAML for user configuration, TOML for tool configuration
- **Validation**: Pydantic models for all configuration
- **Environment**: Environment variable support
- **Defaults**: Sensible defaults with override capability

### Settings Management
- **User preferences**: Persistent user settings
- **Project settings**: Per-project configuration
- **Global settings**: System-wide defaults

## External Dependencies

### LLM Providers
- **Primary**: OpenAI API (GPT-4)
- **Alternative**: Google Gemini
- **Strategy**: Provider abstraction for easy switching

### Additional Services
- **HTTP client**: httpx (async-first HTTP client)
- **File handling**: pathlib (standard library)
- **Data validation**: Pydantic throughout

## Development Workflow

### Development Process
1. **Setup**: uv-based environment initialization
2. **Development**: Type-safe development with real-time feedback
3. **Testing**: Comprehensive test suite execution
4. **Quality**: Pre-commit hooks for code quality
5. **CI/CD**: Automated testing and deployment

### Code Quality Gates
- **Pre-commit**: Local quality checks
- **CI pipeline**: Comprehensive testing matrix
- **Coverage**: Minimum coverage requirements
- **Type safety**: Strict type checking
- **Security**: Automated security scanning

## Migration Strategy

### From Traditional Stack
- **Package management**: Poetry → uv migration path
- **Code quality**: Gradual Ruff adoption
- **Type checking**: Incremental type annotation
- **Testing**: pytest plugin integration

### Future Considerations
- **Python 3.12/3.13**: Evaluation timeline
- **New tools**: Continuous evaluation of emerging tools
- **Performance**: Ongoing optimization opportunities
