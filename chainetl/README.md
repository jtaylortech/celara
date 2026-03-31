# ChainETL

Production-grade blockchain data pipelines. Extract blockchain data to data warehouses with ease.

**Supported Chains**: Ethereum, Base L2

## What is ChainETL?

ChainETL is an open-source tool for extracting, transforming, and loading blockchain data into analytics-ready formats. Think of it as the Airbyte/Fivetran for blockchain data.

### Key Features

- **Multi-Chain Support**: Ethereum and Base L2 with more chains coming soon
- **Resumable Syncs**: Automatic checkpointing to resume from where you left off
- **Batch Processing**: Efficiently sync thousands of blocks at once
- **Reorg Detection**: Handles chain reorganizations automatically
- **Type-Safe**: Full type hints with mypy strict mode
- **Production Ready**: Retry logic, structured logging, comprehensive tests
- **Easy to Use**: Simple CLI commands to get started in minutes

## Quick Start

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- RPC endpoint for your blockchain (public or private)

### Installation

Install from PyPI (recommended):

```bash
pip install chainetl
```

Or install from source using uv:

```bash
# Clone the repository
git clone https://github.com/jtaylortech/celara-homepage.git
cd celara-homepage/chainetl

# Install dependencies
uv sync

# Copy environment template
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
DATABASE_URL=postgresql://localhost/chainetl_dev
ETHEREUM_RPC_URL=https://eth.llamarpc.com
BASE_RPC_URL=https://mainnet.base.org
```

### Docker Installation (Alternative)

Use Docker for easy deployment with zero configuration:

```bash
# Clone the repository
git clone https://github.com/jtaylortech/celara-homepage.git
cd celara-homepage/chainetl

# Create .env file (optional, uses public RPCs by default)
cat > .env <<EOF
ETHEREUM_RPC_URL=https://eth.llamarpc.com
BASE_RPC_URL=https://mainnet.base.org
EOF

# Start ChainETL + PostgreSQL
docker-compose up -d

# View logs
docker-compose logs -f chainetl-ethereum

# Check status
docker-compose exec chainetl-ethereum chainetl status --chain ethereum

# Stop services
docker-compose down
```

**Multi-chain setup:**
```bash
# Sync both Ethereum and Base simultaneously
docker-compose --profile multi-chain up -d
```

**Benefits of Docker:**
- No Python installation required
- Automatic PostgreSQL setup
- Easy scaling and deployment
- Isolated environment

### First Sync

Sync 10 Ethereum blocks:

```bash
uv run chainetl sync --chain ethereum --start-block 18000000 --count 10
```

Check the status:

```bash
uv run chainetl status --chain ethereum
```

## Usage

### Syncing Blocks

Extract blocks from Ethereum:
```bash
# Sync a single block
uv run chainetl sync --chain ethereum --start-block 18000000

# Sync 100 blocks
uv run chainetl sync --chain ethereum --start-block 18000000 --count 100

# Sync from latest block
uv run chainetl sync --chain ethereum
```

Extract blocks from Base L2:
```bash
# Sync a single block
uv run chainetl sync --chain base --start-block 10000000

# Sync 100 blocks
uv run chainetl sync --chain base --start-block 10000000 --count 100
```

### Resume from Checkpoint

Continue syncing from where you left off:
```bash
# Resume Ethereum sync
uv run chainetl sync --chain ethereum --resume --count 1000

# Resume Base L2 sync
uv run chainetl sync --chain base --resume --count 1000
```

### Check Status

View sync progress and checkpoint information:
```bash
uv run chainetl status --chain ethereum
uv run chainetl status --chain base
```

Example output:
```
ChainETL Status:
  Chain: ethereum
  Status: Ready
  RPC: https://eth.llamarpc.com
  Database: postgresql://localhost/chainetl_dev

Checkpoint:
  Last synced block: 18000999
  Last synced hash: 0x7f7889c3686d7f560dd690aeb2a10b49e3a76844543cf78cc0dfe4687e2985d2
  Synced at: 2025-11-16 00:22:02
  Status: active
```

### Multi-Chain Setup

Run both chains simultaneously with independent checkpoints:

```bash
# Terminal 1: Ethereum sync
uv run chainetl sync --chain ethereum --resume --count 100

# Terminal 2: Base sync
uv run chainetl sync --chain base --resume --count 500
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Database connection (required)
DATABASE_URL=postgresql://localhost/chainetl_dev

# Ethereum RPC endpoint (required for ethereum chain)
ETHEREUM_RPC_URL=https://eth.llamarpc.com

# Base L2 RPC endpoint (required for base chain)
BASE_RPC_URL=https://mainnet.base.org

# Optional: Logging configuration
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Database Setup

ChainETL uses PostgreSQL to store blockchain data. Create a database:

```bash
# Using psql
createdb chainetl_dev

# Or using SQL
psql -c "CREATE DATABASE chainetl_dev;"
```

The schema will be created automatically on first run.

### RPC Endpoints

You can use public RPC endpoints or run your own node:

**Ethereum Public RPCs:**
- `https://eth.llamarpc.com` (LlamaNodes)
- `https://rpc.ankr.com/eth` (Ankr)
- `https://ethereum.publicnode.com` (PublicNode)

**Base L2 Public RPCs:**
- `https://mainnet.base.org` (Official)
- `https://base.llamarpc.com` (LlamaNodes)
- `https://base.publicnode.com` (PublicNode)

## Architecture

### Components

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Blockchain │ ───> │   ChainETL  │ ───> │  PostgreSQL │
│   (Source)  │      │  (Extract)  │      │ (Warehouse) │
└─────────────┘      └─────────────┘      └─────────────┘
```

**Extractors**
- Connect to blockchain RPC endpoints
- Extract blocks and transactions
- Handle retries and errors
- Support batch processing

**Loaders**
- Write data to PostgreSQL
- Manage checkpoints for resumability
- Detect and handle chain reorgs
- Ensure data consistency

**Models**
- Pydantic models for type safety
- Validate data from RPC responses
- Provide clean Python interfaces

**CLI**
- Simple commands for syncing and monitoring
- Multi-chain support with independent checkpoints
- Structured logging with progress tracking

### Detailed Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         ChainETL Pipeline                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────────────────────────┐
│              │         │                                  │
│  Ethereum    │◄────────│  EthereumExtractor               │
│  RPC Node    │         │  - extract_block()               │
│              │         │  - extract_blocks()              │
└──────────────┘         │  - extract_latest_block_number() │
                         │                                  │
                         └──────────────┬───────────────────┘
                                        │
┌──────────────┐         ┌──────────────▼───────────────────┐
│              │         │                                  │
│  Base L2     │◄────────│  BaseL2Extractor                 │
│  RPC Node    │         │  - extract_block()               │
│              │         │  - extract_blocks()              │
└──────────────┘         │  - extract_latest_block_number() │
                         │                                  │
                         └──────────────┬───────────────────┘
                                        │
                         ┌──────────────▼───────────────────┐
                         │                                  │
                         │  Block Model (Pydantic)          │
                         │  - Validates RPC response        │
                         │  - Type-safe data structures     │
                         │                                  │
                         └──────────────┬───────────────────┘
                                        │
                         ┌──────────────▼───────────────────┐
                         │                                  │
                         │  PostgresLoader                  │
                         │  - load_block() / load_blocks()  │
                         │  - save_checkpoint()             │
                         │  - detect_reorg()                │
                         │                                  │
                         └──────────────┬───────────────────┘
                                        │
                         ┌──────────────▼───────────────────┐
                         │                                  │
                         │  PostgreSQL Database             │
                         │  ┌────────────────────────────┐  │
                         │  │  blocks                    │  │
                         │  │  - number, hash, timestamp │  │
                         │  │  - parent_hash, gas_*      │  │
                         │  └────────────────────────────┘  │
                         │  ┌────────────────────────────┐  │
                         │  │  checkpoints               │  │
                         │  │  - chain, last_synced_*    │  │
                         │  │  - synced_at, status       │  │
                         │  └────────────────────────────┘  │
                         │                                  │
                         └──────────────────────────────────┘

Key Features:
├── Retry Logic: Exponential backoff for RPC failures
├── Checkpoints: Resume from last synced block per chain
├── Reorg Detection: Compare parent hashes for consistency
├── Batch Processing: Sync multiple blocks efficiently
└── Multi-Chain: Independent pipelines for each blockchain
```

### Database Schema

**blocks** table:
```sql
CREATE TABLE blocks (
    number INTEGER PRIMARY KEY,
    hash VARCHAR(66) NOT NULL,
    parent_hash VARCHAR(66) NOT NULL,
    timestamp INTEGER NOT NULL,
    gas_used BIGINT NOT NULL,
    gas_limit BIGINT NOT NULL
);
```

**checkpoints** table:
```sql
CREATE TABLE checkpoints (
    chain VARCHAR(20) PRIMARY KEY,
    last_synced_block INTEGER NOT NULL,
    last_synced_hash VARCHAR(66) NOT NULL,
    synced_at TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL
);
```

## Development

### Setup

```bash
# Install all dependencies including dev tools
uv sync --all-extras

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Lint code
uv run ruff check .

# Fix linting issues
uv run ruff check --fix .

# Type check
uv run mypy src/

# Format code
uv run ruff format .
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_extractors.py

# Run with verbose output
uv run pytest -v

# Run with coverage report
uv run pytest --cov=src --cov-report=term-missing
```

Current test coverage: **91%** (36 tests)

## Examples

See the `examples/` directory for detailed guides:

- [examples/ethereum.md](examples/ethereum.md) - Complete Ethereum sync guide
- [examples/base.md](examples/base.md) - Complete Base L2 sync guide
- [.env.example](.env.example) - Configuration template

## Documentation

- [Product Documentation](../docs/products/chainetl.md) - Full product overview and roadmap
- [L2 Fields Reference](docs/L2_FIELDS.md) - Layer 2 blockchain field documentation
- [Architecture Guide](../docs/products/chainetl.md#architecture) - Detailed architecture overview

## Troubleshooting

### Common Issues

**Database Connection Error**
```
Error: could not connect to server
```
Solution: Ensure PostgreSQL is running and DATABASE_URL is correct.

**RPC Rate Limits**
```
Error: Too many requests
```
Solution: Use a different RPC provider or run your own node.

**Checkpoint Not Found**
```
Checkpoint: None (no ethereum sync yet)
```
This is normal for first-time syncs. The checkpoint will be created after the first successful sync.

### Getting Help

- Check the [examples/](examples/) directory for usage guides
- Review [docs/L2_FIELDS.md](docs/L2_FIELDS.md) for L2-specific questions
- Open an issue on GitHub for bugs or feature requests

## Performance

### Benchmarks

- Sync speed: 50-100 blocks/second (Ethereum, depends on RPC)
- Sync speed: 100-200 blocks/second (Base L2, faster due to 2s blocks)
- Memory usage: <100MB for typical syncs
- Database size: ~1KB per block (minimal schema)

### Optimization Tips

1. **Use batch syncing**: `--count 1000` is faster than syncing 1 block at a time
2. **Run your own node**: Eliminates RPC rate limits and latency
3. **Use connection pooling**: Configure PostgreSQL for better performance
4. **Monitor RPC health**: Switch endpoints if one becomes slow

## FAQ

### General Questions

**Q: What blockchains are supported?**
A: Currently Ethereum mainnet and Base L2. More chains (Polygon, Arbitrum, Optimism) are planned for future releases.

**Q: Do I need to run my own blockchain node?**
A: No! ChainETL works with any RPC endpoint. You can use free public RPCs or paid services like Alchemy, Infura, or QuickNode.

**Q: How much does it cost to run?**
A: ChainETL is free and open-source. Costs depend on your RPC provider (free public RPCs available) and database hosting.

**Q: Can I use ChainETL in production?**
A: Yes! ChainETL includes production features like checkpoints, retry logic, reorg detection, and comprehensive logging.

### Setup Questions

**Q: What are the system requirements?**
A: Python 3.11+, PostgreSQL database, and an internet connection. Minimal hardware requirements (<100MB RAM for typical usage).

**Q: Can I use SQLite instead of PostgreSQL?**
A: For development and testing, yes. For production, PostgreSQL is recommended for performance and reliability.

**Q: How do I get an RPC endpoint?**
A: Use free public RPCs (see Configuration section) or sign up for services like:
- Alchemy (free tier available)
- Infura (free tier available)
- QuickNode (paid)
- Or run your own Ethereum/Base node

### Usage Questions

**Q: How fast is syncing?**
A: Depends on your RPC endpoint. Typically 50-100 blocks/second for Ethereum, 100-200 blocks/second for Base L2.

**Q: Can I sync multiple chains simultaneously?**
A: Yes! Each chain maintains independent checkpoints. Run separate sync commands or use multiple terminal windows.

**Q: What happens if syncing is interrupted?**
A: Use `--resume` to continue from the last checkpoint. ChainETL automatically saves progress after each batch.

**Q: How do I handle RPC rate limits?**
A: 1) Use `--count` to control batch size, 2) Add delays between batches, 3) Use a paid RPC service, or 4) Run your own node.

### Data Questions

**Q: What data is extracted?**
A: Currently: block number, hash, parent hash, timestamp, gas used, gas limit. Future versions will include transactions, logs, and traces.

**Q: Are L2-specific fields captured?**
A: Basic block data is captured. Advanced L2 fields (L1 batch number, deposit/withdrawal transactions) are documented but not yet persisted. See [docs/L2_FIELDS.md](docs/L2_FIELDS.md).

**Q: How is chain reorganization handled?**
A: ChainETL detects reorgs by comparing parent hashes. Basic handling is implemented - warnings are logged but syncing continues.

**Q: Can I export data to CSV or Parquet?**
A: Not yet, but it's on the roadmap. Currently, data is stored in PostgreSQL and you can export using SQL queries or tools like pgAdmin.

### Development Questions

**Q: How do I add support for a new blockchain?**
A: See [CONTRIBUTING.md](CONTRIBUTING.md) for a guide on implementing new extractors. Most EVM-compatible chains are straightforward to add.

**Q: Can I contribute to ChainETL?**
A: Absolutely! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We welcome bug reports, feature requests, and pull requests.

**Q: How do I run tests?**
A: Run `uv run pytest` for all tests, or `uv run pytest --cov=src` for coverage reports.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Ensure all tests pass (`uv run pytest`)
5. Ensure code quality (`uv run ruff check .` and `uv run mypy src/`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Roadmap

### Current Version: v0.1.0 (Phase 3 Complete)

- Multi-chain support (Ethereum, Base L2)
- Resumable syncs with checkpoints
- Batch processing
- Reorg detection
- PostgreSQL loader

### Future Enhancements

- Additional chains (Polygon, Arbitrum, Optimism, Solana)
- Additional loaders (BigQuery, Snowflake, S3/Parquet)
- Transaction and log extraction
- dbt transformation layer
- API server mode
- Real-time streaming mode

See [docs/products/chainetl.md](../docs/products/chainetl.md) for the full roadmap.

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.

## Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) for the CLI
- Uses [Pydantic](https://docs.pydantic.dev/) for data validation
- Powered by [SQLAlchemy](https://www.sqlalchemy.org/) for database operations
- Structured logging with [structlog](https://www.structlog.org/)

## Support

- GitHub Issues: Bug reports and feature requests
- Documentation: See `docs/` and `examples/` directories
- Email: Contact the maintainers for enterprise support

---

**Built by the Celara team** | [Documentation](../docs/products/chainetl.md) | [Contributing](CONTRIBUTING.md) | [License](LICENSE)
