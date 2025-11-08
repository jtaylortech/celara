# ChainETL

Blockchain data pipelines. Extract blockchain data to data warehouses.

## Quick Start

```bash
# Install dependencies
uv sync

# Run CLI
uv run chainetl sync --help

# Extract a block
uv run chainetl sync --chain ethereum --start-block 18000000

# Run tests
uv run pytest
```

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Run linter
uv run ruff check .

# Run type checker
uv run mypy src/

# Format code
uv run ruff format .
```

## Architecture

- **Extractors**: Connect to blockchain RPCs and extract data
- **Loaders**: Write data to destinations (Postgres, files, etc.)
- **Models**: Pydantic models for type-safe data handling
- **CLI**: Typer-based command-line interface

## Documentation

See [docs/products/chainetl.md](../docs/products/chainetl.md) for full product documentation.

## License

Apache 2.0
