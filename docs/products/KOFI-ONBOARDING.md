# Welcome to Celara, Kofi

**Your Mission:** Build ChainETL — the best blockchain data pipeline tool in the world.

**Project Location:** `/Users/jarredet/Code/projects/celara-homepage/chainetl`

This guide will take you from zero to shipping production code. No prior experience required.

---

## Table of Contents

1. [What You're Building](#what-youre-building)
2. [macOS Setup](#macos-setup)
3. [Git Basics](#git-basics)
4. [Development Workflow](#development-workflow)
5. [Python Fundamentals](#python-fundamentals)
6. [Working with ChainETL](#working-with-chainetl)
7. [Getting Help](#getting-help)

---

## What You're Building

**ChainETL** = Extract blockchain data → Load into databases → Enable analytics

**Why it matters:**
- Blockchain data is hard to access and analyze
- Companies pay $10K+/month for this capability
- You're building the open-source standard

**Your impact:**
- Thousands of developers will use your code
- DAOs and protocols will make decisions based on your data
- You're learning production-grade software engineering

**Read this first:** [ChainETL Product Doc](./chainetl.md)

---

## macOS Setup

### Step 1: Install Homebrew (Package Manager)

Homebrew lets you install developer tools easily.

```bash
# Open Terminal (Cmd + Space, type "Terminal")
# Paste this command:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Follow the instructions it prints at the end
# Usually you need to run these two commands:
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# Verify it works:
brew --version
# Should print: Homebrew 4.x.x
```

### Step 2: Install Git

Git tracks changes to your code and lets you collaborate.

```bash
# Install Git
brew install git

# Verify it works:
git --version
# Should print: git version 2.x.x

# Configure your identity (IMPORTANT - use these exact values):
git config --global user.name "jtaylortech"
git config --global user.email "jarrede20@gmail.com"

# Verify your config:
git config --global user.name
git config --global user.email
```

### Step 3: Install Python with uv

`uv` is a modern, fast Python package manager.

```bash
# Install uv
brew install uv

# Verify it works:
uv --version
# Should print: uv 0.x.x

# uv will automatically install Python when you create a project
```

### Step 4: Install VS Code (Code Editor)

```bash
# Install VS Code
brew install --cask visual-studio-code

# Open VS Code
code

# Install these extensions (click Extensions icon on left sidebar):
# 1. Python (by Microsoft)
# 2. Pylance (by Microsoft)
# 3. Ruff (by Astral)
# 4. GitLens (by GitKraken)
```

### Step 5: Setup SSH for GitHub

SSH lets you push code to GitHub securely.

```bash
# Generate SSH key (press Enter for all prompts):
ssh-keygen -t ed25519 -C "jarrede20@gmail.com"

# Start SSH agent:
eval "$(ssh-agent -s)"

# Add key to agent:
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard:
cat ~/.ssh/id_ed25519.pub | pbcopy

# Now go to GitHub:
# 1. Go to github.com (login if needed)
# 2. Click your profile picture → Settings
# 3. Click "SSH and GPG keys" on left
# 4. Click "New SSH key"
# 5. Title: "Kofi's MacBook"
# 6. Paste the key (Cmd+V)
# 7. Click "Add SSH key"

# Test it works:
ssh -T git@github.com
# Should print: "Hi [username]! You've successfully authenticated..."
```

### Step 6: Install Postgres (Database)

```bash
# Install Postgres
brew install postgresql@16

# Start Postgres (runs in background):
brew services start postgresql@16

# Verify it works:
psql --version
# Should print: psql (PostgreSQL) 16.x

# Create a test database:
createdb chainetl_dev

# Connect to it:
psql chainetl_dev
# You should see: chainetl_dev=#
# Type \q to quit
```

### Step 7: Install Useful Tools

```bash
# httpie - test APIs from terminal
brew install httpie

# jq - parse JSON
brew install jq

# tree - visualize directory structure
brew install tree
```

---

## Git Basics

Git is how you save and share your code. Think of it like "Track Changes" for code.

### Key Concepts

**Repository (repo):** A project folder tracked by Git  
**Commit:** A saved snapshot of your code  
**Branch:** A parallel version of your code  
**Remote:** The version on GitHub  
**Local:** The version on your computer

### Essential Commands

```bash
# ============================================
# GETTING CODE (Do this once)
# ============================================

# Clone a repository (download it):
git clone git@github.com:username/repo.git
cd repo

# ============================================
# DAILY WORKFLOW (Do this every time you code)
# ============================================

# 1. Check what changed:
git status
# Shows: modified files, new files, deleted files

# 2. See specific changes:
git diff
# Shows: line-by-line what changed

# 3. Add files to staging (prepare to save):
git add filename.py          # Add one file
git add .                    # Add all files

# 4. Commit (save a snapshot):
git commit -m "Add ethereum extractor"
# Message should describe WHAT you did

# 5. Push to GitHub (upload your changes):
git push

# ============================================
# GETTING UPDATES (Do this before you start coding)
# ============================================

# Pull latest changes from GitHub:
git pull

# ============================================
# BRANCHES (Parallel versions)
# ============================================

# Create a new branch:
git checkout -b feature/add-base-support

# Switch to existing branch:
git checkout main

# List all branches:
git branch

# Push new branch to GitHub:
git push -u origin feature/add-base-support

# ============================================
# FIXING MISTAKES
# ============================================

# Undo changes to a file (before commit):
git checkout -- filename.py

# Undo last commit (keep changes):
git reset --soft HEAD~1

# See commit history:
git log --oneline

# ============================================
# COMMON SCENARIOS
# ============================================

# Scenario 1: You made changes and want to save them
git status                           # See what changed
git add .                           # Stage all changes
git commit -m "Implement postgres loader"
git push

# Scenario 2: You want to start a new feature
git checkout main                   # Go to main branch
git pull                           # Get latest changes
git checkout -b feature/add-logging # Create new branch
# ... make changes ...
git add .
git commit -m "Add structured logging"
git push -u origin feature/add-logging

# Scenario 3: You want to get JT's latest changes
git checkout main
git pull
git checkout your-branch
git merge main                     # Bring main's changes into your branch

# Scenario 4: You messed up and want to start over
git status                         # See what's wrong
git stash                         # Hide your changes temporarily
git pull                          # Get latest code
git stash pop                     # Bring your changes back
```

### Git Workflow Diagram

```
Your Computer                    GitHub
─────────────                    ──────

  Working Dir  ──add──>  Staging  ──commit──>  Local Repo  ──push──>  Remote Repo
  (edit files)           (git add)              (git commit)           (git push)

                                  Local Repo  <──pull───  Remote Repo
                                               (git pull)
```

### Best Practices

DO:
- Commit often (every 30-60 minutes)
- Write clear commit messages ("Add X", "Fix Y", "Update Z")
- Pull before you start coding
- Push at end of day

DON'T:
- Commit broken code (make sure it runs first)
- Use vague messages ("fix stuff", "updates")
- Work for days without committing
- Push secrets/passwords (use .env files)

---

## Development Workflow

This is your daily routine when building ChainETL.

### Morning Routine (5 minutes)

```bash
# 1. Open Terminal
cd /Users/jarredet/Code/projects/celara-homepage/chainetl

# 2. Get latest changes
git pull

# 3. Check what you're working on
git status
git log --oneline -5

# 4. Open VS Code
code .
```

### Coding Session (2-4 hours)

```bash
# 1. Create a branch for your feature
git checkout -b feature/ethereum-extractor

# 2. Write code in VS Code
# - Edit files
# - Save often (Cmd+S)
# - Run code to test

# 3. Test your code
uv run pytest                    # Run all tests
uv run pytest tests/test_extractors.py  # Run specific test
uv run python -m chainetl.cli sync      # Run the CLI

# 4. Check code quality
uv run ruff check .              # Lint code
uv run mypy src/                 # Type check
uv run ruff format .             # Format code

# 5. Commit your progress
git status                       # See what changed
git add .                        # Stage changes
git commit -m "Implement ethereum block extraction"
```

### End of Day (5 minutes)

```bash
# 1. Make sure everything works
uv run pytest

# 2. Commit any remaining changes
git add .
git commit -m "WIP: working on transaction parsing"

# 3. Push to GitHub
git push

# 4. Document what you did
# - Update your notes
# - Write down any blockers
# - Plan tomorrow's tasks
```

### Weekly Review (30 minutes)

```bash
# 1. Review your progress
git log --oneline --since="1 week ago"

# 2. Clean up branches
git branch                       # List branches
git branch -d old-feature       # Delete merged branches

# 3. Update dependencies
uv sync

# 4. Review open issues/PRs on GitHub
```

---

## Python Fundamentals

Quick reference for Python concepts you'll use in ChainETL.

### Type Hints (Critical for ChainETL)

```python
# Basic types
def get_block(block_number: int) -> dict:
    return {"number": block_number}

# Optional types
from typing import Optional

def get_transaction(tx_hash: str) -> Optional[dict]:
    # Returns dict or None
    return None

# Lists and Dicts
from typing import List, Dict

def get_blocks(start: int, end: int) -> List[Dict[str, any]]:
    return [{"number": i} for i in range(start, end)]
```

### Pydantic Models (Data Validation)

```python
from pydantic import BaseModel, Field

class Block(BaseModel):
    number: int
    hash: str
    timestamp: int
    transactions: List[str] = Field(default_factory=list)

# Usage:
block = Block(number=18000000, hash="0x123...", timestamp=1699999999)
print(block.number)  # 18000000
print(block.model_dump())  # Convert to dict
```

### Async/Await (Concurrent Operations)

```python
import httpx
import asyncio

async def fetch_block(block_number: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://eth.llamarpc.com",
            json={"method": "eth_getBlockByNumber", "params": [hex(block_number), False]}
        )
        return response.json()

# Run async function:
block = asyncio.run(fetch_block(18000000))
```

### Error Handling

```python
import structlog

logger = structlog.get_logger()

def extract_block(block_number: int) -> dict:
    try:
        # Try to get block
        block = fetch_block(block_number)
        return block
    except httpx.HTTPError as e:
        logger.error("http_error", block_number=block_number, error=str(e))
        raise
    except Exception as e:
        logger.exception("unexpected_error", block_number=block_number)
        raise
```

### Testing with pytest

```python
# tests/test_extractors.py
import pytest
from chainetl.extractors.ethereum import EthereumExtractor

def test_extract_block():
    extractor = EthereumExtractor(rpc_url="https://eth.llamarpc.com")
    block = extractor.extract_block(18000000)
    
    assert block.number == 18000000
    assert block.hash.startswith("0x")
    assert len(block.transactions) > 0

def test_extract_invalid_block():
    extractor = EthereumExtractor(rpc_url="https://eth.llamarpc.com")
    
    with pytest.raises(ValueError):
        extractor.extract_block(-1)
```

---

## Working with ChainETL

The project is already set up at `/Users/jarredet/Code/projects/celara-homepage/chainetl`.

### Getting Started

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

# 6. Initialize git (if not already done)
git init
git add .
git commit -m "Initial ChainETL setup"

# 7. Create GitHub repo and push
# Go to github.com/new, create "chainetl" repo
git remote add origin git@github.com:celara/chainetl.git
git branch -M main
git push -u origin main
```

### Project Structure

```
chainetl/
├── src/chainetl/
│   ├── cli.py              # CLI commands (already implemented)
│   ├── config.py           # Configuration (already implemented)
│   ├── extractors/
│   │   ├── base.py         # Base extractor (already implemented)
│   │   └── ethereum.py     # Ethereum extractor (already implemented)
│   ├── loaders/
│   │   ├── base.py         # Base loader (already implemented)
│   │   └── postgres.py     # Postgres loader (already implemented)
│   ├── models/
│   │   └── block.py        # Block model (already implemented)
│   └── utils/
│       └── rpc.py          # RPC client (already implemented)
└── tests/
    └── test_extractors.py  # Tests (already implemented)
```

### Your First Tasks

**Week 1: Get Familiar**
- Read through all the existing code
- Run the tests and make sure they pass
- Try extracting different blocks
- Modify the CLI to add a new option

**Week 2: Add Features**
- Add transaction extraction (not just hashes)
- Implement file-based loader (CSV/Parquet)
- Add retry logic to RPC client
- Write tests for new features

**Week 3: Reliability**
- Add checkpoint system (save progress)
- Handle chain reorgs
- Implement batch processing
- Performance optimization

**Week 4: Multi-Chain**
- Add Base L2 support
- Abstract common patterns
- Update CLI for chain selection
- Add chain-specific tests

---

## Getting Help

### When You're Stuck

**1. Read the error message carefully**
- Python errors tell you exactly what's wrong
- Look at the last line first (the actual error)
- Then look at the traceback (where it happened)

**2. Google it**
- Copy the error message
- Add "python" to your search
- Look for Stack Overflow answers

**3. Use AI assistants**
- ChatGPT, Claude, or GitHub Copilot
- Paste your code + error
- Ask specific questions

**4. Ask JT**
- Discord: #chainetl channel
- GitHub: Open an issue
- Direct message

### Common Issues & Solutions

**Issue: `command not found: uv`**
```bash
# Solution: Install uv
brew install uv
```

**Issue: `ModuleNotFoundError: No module named 'chainetl'`**
```bash
# Solution: Install in editable mode
uv pip install -e .
```

**Issue: `permission denied` when running git**
```bash
# Solution: Check SSH key is added
ssh-add ~/.ssh/id_ed25519
```

**Issue: Tests failing**
```bash
# Solution: Check you're in the right directory
pwd  # Should be /Users/jarredet/Code/projects/chainetl
uv run pytest -v  # Run with verbose output
```

### Learning Resources

**Python:**
- [Official Python Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/) (excellent tutorials)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

**Git:**
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Learn Git Branching](https://learngitbranching.js.org/) (interactive)

**Blockchain:**
- [Ethereum Docs](https://ethereum.org/en/developers/docs/)
- [Base Docs](https://docs.base.org/)

**Testing:**
- [pytest Documentation](https://docs.pytest.org/)
- [Test-Driven Development](https://testdriven.io/)

---

## Your First Week Goals

### Day 1: Setup
- [ ] Install all tools (Homebrew, Git, uv, VS Code, Postgres)
- [ ] Setup SSH key for GitHub
- [ ] Navigate to chainetl project
- [ ] Read ChainETL product doc

### Day 2: Git Practice
- [ ] Initialize git in chainetl project
- [ ] Create GitHub repo
- [ ] Practice: commit, push
- [ ] Create a branch, make changes, merge

### Day 3: Explore Codebase
- [ ] Read through all existing code
- [ ] Run tests and understand what they do
- [ ] Try the CLI commands
- [ ] Extract a few different blocks

### Day 4: First Modification
- [ ] Add a new CLI option
- [ ] Write a test for it
- [ ] Get tests passing
- [ ] Commit and push

### Day 5: First Feature
- [ ] Pick a small feature to add
- [ ] Implement it
- [ ] Write tests
- [ ] Get code review from JT

---

## Next Steps

Once you're comfortable with the basics:

1. **Build Features** (Weeks 1-4)
   - Follow the [ChainETL doc](./chainetl.md) phases
   - Commit code daily
   - Ask questions early and often

2. **Learn by Doing**
   - Read other people's code (check out similar projects)
   - Experiment and break things (that's how you learn)
   - Write tests for everything

3. **Ship It**
   - Get to a working demo ASAP
   - Show JT your progress weekly
   - Launch on GitHub when ready

---

**Remember:** Every expert was once a beginner. You've got this.

**Questions?** Reach out anytime. We're building this together.

— JT & the Celara team
