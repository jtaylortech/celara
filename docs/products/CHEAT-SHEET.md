# ChainETL Development Cheat Sheet

Quick reference for daily development. Print this out or keep it open.

---

## Most Used Commands

```bash
# ============================================
# GIT (Version Control)
# ============================================

# Daily workflow:
git status                              # What changed?
git add .                              # Stage all changes
git commit -m "Add feature X"          # Save snapshot
git push                               # Upload to GitHub
git pull                               # Download from GitHub

# Branching:
git checkout -b feature/my-feature     # Create new branch
git checkout main                      # Switch to main
git merge feature/my-feature           # Merge branch into current

# Undo:
git checkout -- file.py                # Undo changes to file
git reset --soft HEAD~1                # Undo last commit (keep changes)

# ============================================
# UV (Python Package Manager)
# ============================================

uv add package-name                    # Add dependency
uv add --dev package-name              # Add dev dependency
uv sync                                # Install all dependencies
uv run python script.py                # Run Python script
uv run pytest                          # Run tests

# ============================================
# PYTEST (Testing)
# ============================================

uv run pytest                          # Run all tests
uv run pytest -v                       # Verbose output
uv run pytest tests/test_file.py       # Run specific file
uv run pytest -k test_name             # Run specific test
uv run pytest --cov=src                # Run with coverage

# ============================================
# CODE QUALITY
# ============================================

uv run ruff check .                    # Lint code
uv run ruff format .                   # Format code
uv run mypy src/                       # Type check

# ============================================
# POSTGRES
# ============================================

psql chainetl_dev                      # Connect to database
\dt                                    # List tables
\d table_name                          # Describe table
SELECT * FROM blocks LIMIT 10;         # Query data
\q                                     # Quit

# ============================================
# CHAINETL CLI
# ============================================

uv run chainetl sync --help            # Show help
uv run chainetl sync --start-block 18000000
uv run chainetl status
```

---

## Project Structure

```
chainetl/
├── src/chainetl/          # Source code
│   ├── cli.py            # CLI commands
│   ├── config.py         # Configuration
│   ├── extractors/       # Blockchain extractors
│   ├── loaders/          # Database loaders
│   ├── models/           # Data models
│   └── utils/            # Helper functions
├── tests/                # Test files
├── pyproject.toml        # Dependencies
└── README.md            # Documentation
```

---

## Python Patterns

### Type Hints
```python
def function(arg: int) -> str:
    return str(arg)

from typing import Optional, List, Dict
def get_data() -> Optional[Dict[str, List[int]]]:
    return {"numbers": [1, 2, 3]}
```

### Pydantic Models
```python
from pydantic import BaseModel

class Block(BaseModel):
    number: int
    hash: str

block = Block(number=1, hash="0x123")
print(block.number)  # 1
```

### Error Handling
```python
try:
    result = risky_operation()
except ValueError as e:
    logger.error("error", error=str(e))
    raise
```

### Async/Await
```python
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

result = asyncio.run(fetch_data())
```

---

## Testing Patterns

```python
import pytest

# Basic test
def test_addition():
    assert 1 + 1 == 2

# Test with fixture
@pytest.fixture
def extractor():
    return EthereumExtractor(rpc_url="https://eth.llamarpc.com")

def test_extract_block(extractor):
    block = extractor.extract_block(18000000)
    assert block.number == 18000000

# Test exception
def test_invalid_input():
    with pytest.raises(ValueError):
        process_block(-1)
```

---

## Debugging Tips

### Print Debugging
```python
print(f"Block number: {block.number}")
print(f"Type: {type(block)}")
print(f"Dict: {block.model_dump()}")
```

### Logging
```python
import structlog
logger = structlog.get_logger()

logger.info("processing_block", block_number=18000000)
logger.error("failed", error=str(e))
```

### Python Debugger
```python
import pdb; pdb.set_trace()  # Pause execution here
# Commands: n (next), s (step), c (continue), p variable (print)
```

---

## Common Errors

### `ModuleNotFoundError`
```bash
# Solution: Install dependencies
uv sync
```

### `ImportError: cannot import name 'X'`
```bash
# Solution: Check your imports and file structure
# Make sure __init__.py exists in directories
```

### `TypeError: 'NoneType' object is not subscriptable`
```python
# Problem: Trying to access None
data = None
print(data["key"])  # Error

# Solution: Check for None first
if data is not None:
    print(data["key"])  # Safe
```

### `IndentationError`
```python
# Problem: Inconsistent indentation
def function():
  print("2 spaces")
    print("4 spaces")  # Error

# Solution: Use consistent indentation (4 spaces)
def function():
    print("4 spaces")
    print("4 spaces")  # Correct
```

---

## Daily Checklist

### Morning (5 min)
- [ ] `cd chainetl`
- [ ] `git pull`
- [ ] `code .` (open VS Code)
- [ ] Review yesterday's notes

### Before Committing (2 min)
- [ ] `uv run pytest` (tests pass)
- [ ] `uv run ruff check .` (no lint errors)
- [ ] `uv run mypy src/` (no type errors)

### End of Day (5 min)
- [ ] `git add .`
- [ ] `git commit -m "Descriptive message"`
- [ ] `git push`
- [ ] Write notes on progress

---

## Quick Links

**Documentation:**
- [ChainETL Product Doc](./chainetl.md)
- [Onboarding Guide](./KOFI-ONBOARDING.md)
- [Python Docs](https://docs.python.org/3/)
- [Pydantic Docs](https://docs.pydantic.dev/)

**Tools:**
- [Ethereum RPC Docs](https://ethereum.org/en/developers/docs/apis/json-rpc/)
- [Base RPC Docs](https://docs.base.org/tools/node-providers/)
- [pytest Docs](https://docs.pytest.org/)

**Help:**
- Google: "python [your question]"
- Stack Overflow: stackoverflow.com
- ChatGPT/Claude: Paste error + code

---

## Pro Tips

1. **Commit often** — Every 30-60 minutes
2. **Test as you go** — Don't wait until the end
3. **Read error messages** — They tell you exactly what's wrong
4. **Google everything** — Every developer does this
5. **Ask for help early** — Don't struggle for hours
6. **Take breaks** — Your brain needs rest
7. **Celebrate wins** — Got a test passing? That's progress

---

**Keep this open while coding**
