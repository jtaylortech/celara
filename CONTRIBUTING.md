# Contributing to Celara

Thank you for contributing! Celara is open-source DevOps tooling for decentralized systems.

## Setup

```bash
git clone https://github.com/jtaylortech/celara-homepage.git
cd celara-homepage

# Python products (pick any)
cd chainetl && uv sync && uv run pytest

# Marketing site
cd web && npm install && npm run dev
```

## Project Structure

```
celara-homepage/
├── chainetl/       # Blockchain data pipelines (Python)
├── chainops/       # Validator deployment (Python)
├── chainwatch/     # Prometheus exporter (Python)
├── securitykit/    # Node security scanner (Python)
├── daoform/        # Governance engine (Python)
└── web/            # Next.js marketing site + docs
```

## Workflow

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Make changes
4. Run tests: `uv run pytest`
5. Run lint: `uv run ruff check .`
6. Commit: `feat: your description`
7. Push and open a PR

## Commit Messages

```
<type>: <description>

Types: feat, fix, docs, refactor, test, chore
```

## Code Standards

- Python 3.11+, type hints, mypy strict
- Ruff for linting
- Pytest for tests
- Pydantic for data models

## License

By contributing, you agree your work is licensed under Apache 2.0.
