# ChainETL

Production-grade blockchain data pipelines for EVM chains.

[![CI](https://github.com/jtaylortech/celara-homepage/actions/workflows/chainetl-ci.yml/badge.svg)](https://github.com/jtaylortech/celara-homepage/actions/workflows/chainetl-ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

---

## What it does

Extract blocks, transactions, logs, and token transfers from any EVM chain and load them into PostgreSQL. Resumable syncs, reorg detection, and batch processing built in.

**Supported chains**: Ethereum · Base · Polygon · Arbitrum

## Quick Start

```bash
cd chainetl
uv sync
cp .env.example .env  # Edit with your RPC URLs + database

# Sync 10 Ethereum blocks
uv run chainetl sync --chain ethereum --start-block 18000000 --count 10

# Sync Polygon
uv run chainetl sync --chain polygon --start-block 50000000 --count 10

# Resume from last checkpoint
uv run chainetl sync --chain ethereum --resume --count 1000

# Check sync status
uv run chainetl status --chain ethereum

# List supported chains
uv run chainetl chains
```

## Features

- **4 EVM chains** — Ethereum, Base, Polygon, Arbitrum
- **Resumable syncs** — Checkpoint-based, pick up where you left off
- **Batch processing** — Progress bars for large syncs
- **Reorg detection** — Catches chain reorganizations
- **Token parsing** — ERC-20 and ERC-721 transfer extraction
- **Type-safe** — Pydantic models, mypy strict, full type hints
- **Tested** — 53 tests, 82% coverage, CI on Python 3.11–3.13

## Architecture

```
chainetl/
├── extractors/       # Chain-specific data extraction
│   ├── evm.py        # Unified EVM extractor (all chains)
│   ├── ethereum.py   # Ethereum wrapper
│   ├── base_l2.py    # Base L2 wrapper
│   ├── polygon.py    # Polygon wrapper
│   └── arbitrum.py   # Arbitrum wrapper
├── loaders/          # Data loading destinations
│   └── postgres.py   # PostgreSQL with SQLAlchemy
├── models/           # Pydantic data models
│   ├── block.py      # Block model
│   ├── transaction.py # Transaction (legacy + EIP-1559)
│   ├── log.py        # Event logs
│   ├── token_transfer.py # ERC-20/721 transfers
│   └── checkpoint.py # Sync checkpoints
├── utils/            # Shared utilities
│   ├── rpc.py        # JSON-RPC client
│   ├── retry.py      # Exponential backoff
│   └── token_parser.py # Token event parsing
└── cli.py            # Typer CLI
```

## Configuration

Copy `.env.example` to `.env`:

```bash
ETHEREUM_RPC_URL=https://eth.llamarpc.com
BASE_RPC_URL=https://mainnet.base.org
POLYGON_RPC_URL=https://polygon-rpc.com
ARBITRUM_RPC_URL=https://arb1.arbitrum.io/rpc
DATABASE_URL=postgresql://localhost/chainetl_dev
LOG_LEVEL=INFO
```

## Development

```bash
uv sync --dev
uv run pytest -v              # Run tests
uv run ruff check .           # Lint
uv run mypy .                 # Type check
```

## Adding a New Chain

Any EVM-compatible chain is a 3-line file:

```python
# extractors/optimism.py
from chainetl.extractors.evm import EVMExtractor

class OptimismExtractor(EVMExtractor):
    def __init__(self, rpc_url: str) -> None:
        super().__init__(rpc_url, chain="optimism")
```

Then add it to `config.py` and `cli.py`'s `SUPPORTED_CHAINS` dict.

## License

Apache 2.0 — See [LICENSE](LICENSE)

---

Part of [Celara](https://celara.dev) — open-source DevOps tooling for decentralized systems.
