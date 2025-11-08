# ChainETL - Start Here

Welcome, Kofi. This project is ready for you to start building.

## Quick Start

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
```

## Documentation

All documentation is in the docs/products/ directory:

**Essential Reading:**
1. [ChainETL Product Doc](../docs/products/chainetl.md) - What you're building
2. [Onboarding Guide](../docs/products/KOFI-ONBOARDING.md) - Complete setup guide
3. [Cheat Sheet](../docs/products/CHEAT-SHEET.md) - Quick reference
4. [Project Reference](../docs/products/PROJECT-TEMPLATE.md) - Architecture details

## What's Already Built

The foundation is complete:
- RPC client for blockchain communication
- Ethereum extractor
- Postgres loader
- CLI with sync and status commands
- Tests with pytest
- Type checking with mypy
- Linting with ruff

## Your First Tasks

**Week 1: Get Familiar**
- Read all the documentation
- Run the existing code
- Understand the architecture
- Make a small change and commit it

**Week 2: Add Features**
- Extract full transaction objects (not just hashes)
- Add file-based loader (CSV/Parquet)
- Implement retry logic
- Write tests

**Week 3: Reliability**
- Add checkpoint system
- Handle chain reorgs
- Batch processing
- Performance optimization

**Week 4: Multi-Chain**
- Add Base L2 support
- Abstract common patterns
- Update CLI
- Add tests

## Getting Help

- Read the error messages carefully
- Google the error + "python"
- Ask JT on Discord or GitHub
- Check the documentation

## Daily Workflow

```bash
# Morning
cd /Users/jarredet/Code/projects/celara-homepage/chainetl
git pull
code .

# During coding
git checkout -b feature/my-feature
# ... make changes ...
uv run pytest
git add .
git commit -m "Add feature X"

# End of day
git push
```

## Success Metrics

You're doing great if:
- Tests pass
- Code is type-safe (mypy passes)
- Commits are daily
- Features work end-to-end

---

**Let's build the best blockchain data pipeline tool.**

Questions? Ask JT anytime.
