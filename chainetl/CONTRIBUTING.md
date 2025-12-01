# Contributing to ChainETL

Thank you for your interest in contributing to ChainETL! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

1. **Clear title**: Describe the issue concisely
2. **Steps to reproduce**: Provide detailed steps
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Environment**: OS, Python version, ChainETL version
6. **Logs**: Include relevant error messages or logs

Example:
```
Title: Checkpoint not saved after successful sync

Steps to reproduce:
1. Run `chainetl sync --chain ethereum --start-block 18000000`
2. Sync completes successfully
3. Run `chainetl status --chain ethereum`
4. Checkpoint shows as None

Expected: Checkpoint should be saved
Actual: Checkpoint is null
Environment: macOS 14, Python 3.11, ChainETL main branch
Logs: [attach logs]
```

### Suggesting Features

We welcome feature suggestions! Please open an issue with:

1. **Use case**: Describe the problem you're trying to solve
2. **Proposed solution**: How you'd like it to work
3. **Alternatives**: Other approaches you've considered
4. **Priority**: How important is this to you?

### Pull Requests

We love pull requests! Here's the process:

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/celara-homepage.git
cd celara-homepage/chainetl
```

### 2. Install Dependencies

```bash
# Install using uv (recommended)
uv sync --all-extras

# Or using pip
pip install -e ".[dev]"
```

### 3. Set Up Pre-Commit Hooks (Optional)

```bash
# Install pre-commit
uv pip install pre-commit

# Set up git hooks
pre-commit install
```

### 4. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b fix/bug-description
```

## Development Workflow

### Making Changes

1. **Write code**: Implement your feature or fix
2. **Add tests**: Ensure your code is tested
3. **Update docs**: Update relevant documentation
4. **Run checks**: Ensure all quality checks pass

### Code Style

We follow strict code quality standards:

**Linting with Ruff:**
```bash
# Check for issues
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

**Type Checking with Mypy:**
```bash
# Run type checker
uv run mypy src/

# Should show: Success: no issues found
```

**Code Standards:**
- Use type hints for all function parameters and return values
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes
- Follow PEP 8 style guide

### Writing Tests

All new code should include tests:

**Test Structure:**
```python
def test_feature_description() -> None:
    """Test that feature works as expected."""
    # Arrange
    extractor = EthereumExtractor(rpc_url="https://eth.llamarpc.com")

    # Act
    result = extractor.extract_block(18000000)

    # Assert
    assert result.number == 18000000
    assert result.hash.startswith("0x")
```

**Running Tests:**
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_extractors.py

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Target: >85% coverage
```

**Test Categories:**
- Unit tests: Test individual functions/classes
- Integration tests: Test component interactions
- End-to-end tests: Test full workflows

### Documentation

Update documentation when adding features:

1. **Docstrings**: Add/update function and class docstrings
2. **README.md**: Update if adding user-facing features
3. **examples/**: Add examples for new functionality
4. **docs/**: Update technical documentation

**Docstring Format:**
```python
def extract_block(self, block_number: int) -> Block:
    """Extract a single block from the blockchain.

    Args:
        block_number: Block number to extract

    Returns:
        Block data

    Raises:
        ValueError: If block not found
    """
    pass
```

## Commit Guidelines

### Commit Messages

Follow conventional commit format:

```
type(scope): short description

Longer description if needed.

- Bullet points for details
- More context

Closes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Examples:**
```
feat(base): add Base L2 extractor support

Implements BaseL2Extractor class with full EVM compatibility.
Includes tests and documentation.

Closes #42
```

```
fix(loader): handle null parent_hash in reorg detection

Previously crashed when parent_hash was None. Now handles
this edge case gracefully.

Fixes #38
```

### Commit Best Practices

- Keep commits focused and atomic
- Write clear, descriptive messages
- Reference issues when applicable
- Don't include unrelated changes

## Pull Request Process

### Before Submitting

Checklist before opening a PR:

- [ ] All tests passing (`uv run pytest`)
- [ ] Code linted (`uv run ruff check .`)
- [ ] Type checking passing (`uv run mypy src/`)
- [ ] Documentation updated
- [ ] Examples added (if applicable)
- [ ] CHANGELOG.md updated (if applicable)

### Opening a Pull Request

1. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open PR on GitHub**: Click "Compare & pull request"

3. **Fill out the PR template**:
   - Describe what changed and why
   - Reference related issues
   - Include screenshots/examples if relevant
   - Note any breaking changes

4. **Request review**: Tag relevant maintainers

### PR Title Format

Use conventional commit format:

```
feat(extractors): add Polygon support
fix(cli): handle keyboard interrupts gracefully
docs(readme): update installation instructions
```

### Code Review

**What to Expect:**
- Maintainers will review your code
- You may be asked to make changes
- Discussion about implementation approaches
- Approval when ready to merge

**Responding to Feedback:**
- Be open to suggestions
- Ask questions if unclear
- Make requested changes promptly
- Push updates to the same branch

### After Approval

Once approved:
1. Maintainer will merge your PR
2. Your contribution will be in the next release
3. You'll be added to contributors list

## Development Tips

### Running Live Tests

Test against live blockchains:

```bash
# Ethereum mainnet
uv run chainetl sync --chain ethereum --start-block 18000000 --count 1

# Base L2
uv run chainetl sync --chain base --start-block 10000000 --count 1
```

### Debugging

Use structured logging:

```python
import structlog

logger = structlog.get_logger()
logger.info("processing_block", block_number=block_number)
logger.error("extraction_failed", error=str(e), block=block_number)
```

### Testing Database Operations

Use SQLite for fast testing:

```python
from chainetl.loaders.postgres import PostgresLoader

# In-memory SQLite for tests
loader = PostgresLoader("sqlite:///:memory:")
```

## Project Structure

```
chainetl/
├── src/chainetl/          # Source code
│   ├── cli.py             # CLI commands
│   ├── config.py          # Configuration
│   ├── extractors/        # Blockchain extractors
│   ├── loaders/           # Data loaders
│   ├── models/            # Pydantic models
│   └── utils/             # Utilities
├── tests/                 # Test suite
├── examples/              # Usage examples
├── docs/                  # Documentation
└── README.md              # Project readme
```

## Adding a New Chain

To add support for a new blockchain:

1. **Create extractor** in `src/chainetl/extractors/`:
   ```python
   class PolygonExtractor(BaseExtractor):
       def chain_name(self) -> str:
           return "polygon"
       # ... implement required methods
   ```

2. **Update CLI** in `src/chainetl/cli.py`:
   ```python
   elif chain == "polygon":
       extractor = PolygonExtractor(rpc_url=settings.polygon_rpc_url)
   ```

3. **Add tests** in `tests/test_extractors.py`

4. **Update documentation**:
   - README.md
   - examples/polygon.md
   - .env.example

## Getting Help

**Questions?**
- Open a GitHub Discussion for general questions
- Comment on relevant issues
- Reach out to maintainers

**Stuck?**
- Review existing code for examples
- Check the documentation
- Ask in your PR or issue

## Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to ChainETL!

---

**Questions?** Open an issue or discussion on GitHub.
