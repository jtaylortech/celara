# ChainETL

Blockchain data pipelines. Extract blockchain data to data warehouses.

**Supported Chains**: Ethereum, Base L2

## Quick Start

```bash
# Install dependencies
uv sync

# Run CLI
uv run chainetl sync --help

# Extract Ethereum blocks
uv run chainetl sync --chain ethereum --start-block 18000000 --count 10

# Extract Base L2 blocks
uv run chainetl sync --chain base --start-block 10000000 --count 10

# Resume from last checkpoint
uv run chainetl sync --chain ethereum --resume --count 100

# Check sync status
uv run chainetl status --chain ethereum
uv run chainetl status --chain base

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
  - Abstract `BaseExtractor` interface for multi-chain support
  - `EthereumExtractor` for Ethereum mainnet
  - `BaseL2Extractor` for Base L2 blockchain
- **Loaders**: Write data to destinations (Postgres, files, etc.)
  - Multi-chain checkpoint system for resumable syncs
  - Reorg detection and handling
- **Models**: Pydantic models for type-safe data handling
- **CLI**: Typer-based command-line interface with multi-chain support

## Documentation

See [docs/products/chainetl.md](../docs/products/chainetl.md) for full product documentation.

## License

Apache 2.0
