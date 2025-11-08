# ChainETL Project Reference

The ChainETL project is already set up and ready to use at:

**Location:** `/Users/jarredet/Code/projects/celara-homepage/chainetl`

---

## Project Structure

```
chainetl/
├── pyproject.toml           # Dependencies & config (DONE)
├── README.md                # Project overview (DONE)
├── .gitignore              # Git ignore rules (DONE)
├── src/
│   └── chainetl/
│       ├── __init__.py     # Package init (DONE)
│       ├── cli.py          # CLI commands (DONE)
│       ├── config.py       # Configuration (DONE)
│       ├── extractors/
│       │   ├── __init__.py (DONE)
│       │   ├── base.py     # Base extractor (DONE)
│       │   └── ethereum.py # Ethereum extractor (DONE)
│       ├── loaders/
│       │   ├── __init__.py (DONE)
│       │   ├── base.py     # Base loader (DONE)
│       │   └── postgres.py # Postgres loader (DONE)
│       ├── models/
│       │   ├── __init__.py (DONE)
│       │   └── block.py    # Block model (DONE)
│       └── utils/
│           ├── __init__.py (DONE)
│           └── rpc.py      # RPC client (DONE)
└── tests/
    ├── __init__.py         (DONE)
    └── test_extractors.py  # Extractor tests (DONE)
```

---

## Getting Started

```bash
# 1. Navigate to project
cd /Users/jarredet/Code/projects/celara-homepage/chainetl

# 2. Install dependencies
uv sync --all-extras

# 3. Create database
createdb chainetl_dev

# 4. Run tests
uv run pytest

# 5. Try the CLI
uv run chainetl status
uv run chainetl sync --start-block 18000000

# 6. Check database
psql chainetl_dev
SELECT * FROM blocks;
\q
```

---

## What's Already Implemented

### Core Infrastructure
- **RPC Client** (`src/chainetl/utils/rpc.py`)
  - JSON-RPC calls with error handling
  - Timeout support
  - Context manager for cleanup

- **Configuration** (`src/chainetl/config.py`)
  - Pydantic settings
  - Environment variable support
  - Default RPC endpoints

### Data Models
- **Block Model** (`src/chainetl/models/block.py`)
  - Type-safe Pydantic model
  - RPC response parser
  - Validation

### Extractors
- **Base Extractor** (`src/chainetl/extractors/base.py`)
  - Abstract interface
  - Standard methods

- **Ethereum Extractor** (`src/chainetl/extractors/ethereum.py`)
  - Block extraction
  - Latest block number
  - Structured logging

### Loaders
- **Base Loader** (`src/chainetl/loaders/base.py`)
  - Abstract interface

- **Postgres Loader** (`src/chainetl/loaders/postgres.py`)
  - SQLAlchemy models
  - Automatic table creation
  - Upsert logic (merge)

### CLI
- **Commands** (`src/chainetl/cli.py`)
  - `chainetl sync` - Extract and load blocks
  - `chainetl status` - Show configuration
  - Typer-based with help text

### Tests
- **Extractor Tests** (`tests/test_extractors.py`)
  - Block extraction test
  - Latest block number test
  - Invalid block test
  - pytest fixtures

---

## Next Steps for Development

### Week 1: Familiarization
- Read through all existing code
- Run tests and understand coverage
- Try extracting different blocks
- Experiment with the CLI

### Week 2: Enhancements
- Add transaction extraction (full tx objects, not just hashes)
- Implement file-based loader (CSV/Parquet)
- Add retry logic with exponential backoff
- Write tests for new features

### Week 3: Reliability
- Implement checkpoint system (save/resume progress)
- Handle chain reorganizations
- Add batch processing for multiple blocks
- Performance profiling and optimization

### Week 4: Multi-Chain
- Add Base L2 extractor
- Abstract common patterns
- Update CLI for chain selection
- Add chain-specific tests

---

## Code Quality Standards

All code follows these standards:

**Type Safety:**
- Full type hints on all functions
- mypy strict mode enabled
- No `Any` types without justification

**Testing:**
- >80% code coverage
- Unit tests for all extractors/loaders
- Integration tests for CLI commands

**Code Style:**
- ruff for linting and formatting
- 100 character line length
- Docstrings on all public functions

**Error Handling:**
- Structured logging with structlog
- Proper exception handling
- Informative error messages

---

## Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/add-transactions

# 2. Make changes
# Edit files in VS Code

# 3. Run quality checks
uv run ruff check .
uv run mypy src/
uv run pytest

# 4. Commit
git add .
git commit -m "Add transaction extraction"

# 5. Push
git push -u origin feature/add-transactions

# 6. Open PR on GitHub for review
```

---

## Useful Commands

```bash
# Run specific test
uv run pytest tests/test_extractors.py::test_extract_block -v

# Run with coverage report
uv run pytest --cov=src/chainetl --cov-report=html
open htmlcov/index.html

# Format code
uv run ruff format .

# Type check
uv run mypy src/ --show-error-codes

# Run CLI in debug mode
uv run python -m pdb -m chainetl.cli sync --start-block 18000000
```

---

## Architecture Decisions

### Why These Technologies?

**Python 3.11+**
- Modern type hints (union types with `|`)
- Better performance
- Excellent blockchain library ecosystem

**uv**
- 10-100x faster than pip
- Built-in virtual environment management
- Lock file for reproducible builds

**Typer**
- Type-safe CLI framework
- Automatic help generation
- Better than argparse/click

**Pydantic**
- Runtime type validation
- JSON serialization
- Settings management

**SQLAlchemy**
- Database abstraction
- Migration support (Alembic)
- Type-safe queries

**structlog**
- Structured logging (JSON)
- Context binding
- Better than stdlib logging

---

## Resources

**Project Documentation:**
- [ChainETL Product Doc](./chainetl.md)
- [Onboarding Guide](./KOFI-ONBOARDING.md)
- [Cheat Sheet](./CHEAT-SHEET.md)

**External Documentation:**
- [Ethereum JSON-RPC](https://ethereum.org/en/developers/docs/apis/json-rpc/)
- [Base Documentation](https://docs.base.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Typer Docs](https://typer.tiangolo.com/)
- [pytest Docs](https://docs.pytest.org/)

---

**The foundation is built. Now let's ship features.**
