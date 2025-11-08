# ChainETL — Blockchain Data Pipelines

**Status:** In Development  
**Owner:** Kofi  
**Launch Target:** Q3 2026  
**Project Location:** `/Users/jarredet/Code/projects/celara-homepage/chainetl`

---

## What is ChainETL?

**One-liner:** Extract blockchain data to data warehouses with production-grade pipelines.

ChainETL is an open-source tool that makes it easy to extract, transform, and load blockchain data into analytics-ready formats. Think of it as the **Airbyte/Fivetran for blockchain data**.

### The Problem

Blockchain data is:
- **Hard to access** — Running full nodes is expensive and complex
- **Difficult to query** — Raw blockchain data isn't analytics-friendly
- **Multi-chain chaos** — Every chain has different APIs and data structures
- **Real-time challenges** — Keeping data fresh requires constant syncing

Current solutions:
- Run your own indexer (expensive, complex)
- Use centralized APIs (rate limits, vendor lock-in)
- Build custom scrapers (maintenance nightmare)

### The Solution

ChainETL provides:
- **One-command setup** — `chainetl init ethereum` and you're running
- **Multi-chain support** — Ethereum, Solana, Polygon, Arbitrum, Base, etc.
- **Multiple destinations** — Postgres, BigQuery, Snowflake, S3, Parquet files
- **Real-time & batch** — Stream live data or backfill historical
- **Transform layer** — Built-in dbt models for common analytics
- **Open source** — Apache 2.0, run anywhere

---

## Architecture

### High-Level Flow

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Blockchain │ ───> │   ChainETL  │ ───> │  Transform  │ ───> │ Data Warehouse│
│   (Source)  │      │  (Extract)  │      │    (dbt)    │      │ (Destination) │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
   Ethereum              Python CLI           SQL Models          Postgres
   Solana                RPC Polling          Aggregations        BigQuery
   Polygon               WebSocket            Metrics             Snowflake
```

### Components

**1. Extractors** (Python)
- Connect to blockchain RPC endpoints
- Poll for new blocks/transactions
- Handle reorgs and retries
- Normalize data across chains

**2. Loaders** (Python)
- Write to various destinations
- Handle batching and buffering
- Ensure idempotency
- Track sync state

**3. Transforms** (dbt/SQL)
- Clean and normalize data
- Calculate metrics (TVL, volume, fees)
- Build dimension tables
- Create analytics views

**4. CLI** (Python + Typer)
- `chainetl init` — Setup new pipeline
- `chainetl sync` — Start syncing data
- `chainetl backfill` — Historical data
- `chainetl status` — Check pipeline health

---

## MVP Scope (First Version)

### Must-Have Features

**Chains:**
- Ethereum (mainnet)
- Base (L2)

**Data Types:**
- Blocks
- Transactions
- Logs/Events
- Traces (future)
- Token transfers (future)

**Destinations:**
- Postgres (local development)
- CSV/Parquet files
- BigQuery (future)
- Snowflake (future)

**Sync Modes:**
- Real-time (poll every block)
- Backfill (historical range)
- Incremental (resume from checkpoint)

**CLI Commands:**
```bash
chainetl init ethereum --destination postgres
chainetl sync --chain ethereum --start-block 18000000
chainetl backfill --chain ethereum --from 17000000 --to 18000000
chainetl status
```

---

## Tech Stack

### Core
- **Language:** Python 3.11+
- **CLI Framework:** Typer (modern, type-safe)
- **HTTP Client:** httpx (async support)
- **Database:** SQLAlchemy (ORM) + Alembic (migrations)
- **Config:** Pydantic Settings (type-safe config)
- **Logging:** structlog (structured logging)

### Data Processing
- **Serialization:** Pydantic models
- **Batch Processing:** Pandas (optional)
- **File Formats:** Parquet (via pyarrow)

### Testing
- **Framework:** pytest
- **Mocking:** pytest-mock
- **Coverage:** pytest-cov (>80% target)

### Development
- **Package Manager:** uv (fast, modern)
- **Linting:** ruff (fast, comprehensive)
- **Type Checking:** mypy (strict mode)
- **Formatting:** ruff format

---

## Project Structure

```
chainetl/
├── README.md                 # Project overview
├── pyproject.toml           # Dependencies & config
├── uv.lock                  # Lock file
├── .python-version          # Python 3.11
├── src/
│   └── chainetl/
│       ├── __init__.py
│       ├── cli.py           # Typer CLI commands
│       ├── config.py        # Pydantic settings
│       ├── extractors/      # Blockchain extractors
│       │   ├── __init__.py
│       │   ├── base.py      # Base extractor class
│       │   ├── ethereum.py  # Ethereum extractor
│       │   └── base_l2.py   # Base L2 extractor
│       ├── loaders/         # Destination loaders
│       │   ├── __init__.py
│       │   ├── base.py      # Base loader class
│       │   ├── postgres.py  # Postgres loader
│       │   └── file.py      # CSV/Parquet loader
│       ├── models/          # Pydantic data models
│       │   ├── __init__.py
│       │   ├── block.py
│       │   ├── transaction.py
│       │   └── log.py
│       └── utils/           # Helpers
│           ├── __init__.py
│           ├── rpc.py       # RPC client
│           └── retry.py     # Retry logic
├── tests/
│   ├── __init__.py
│   ├── test_extractors.py
│   ├── test_loaders.py
│   └── fixtures/            # Test data
├── dbt/                     # dbt transforms (future)
│   └── models/
└── examples/                # Example configs
    ├── ethereum.yaml
    └── base.yaml
```

---

## Development Phases

### Phase 1: Foundation (Weeks 1-2)
**Goal:** Basic CLI + Ethereum extractor + Postgres loader

**Tasks:**
- [ ] Setup project structure
- [ ] Implement CLI skeleton (init, sync, status)
- [ ] Build Ethereum RPC client
- [ ] Create Pydantic models (Block, Transaction, Log)
- [ ] Implement Postgres loader
- [ ] Write tests (>80% coverage)

**Deliverable:** `chainetl sync --chain ethereum` works locally

### Phase 2: Reliability (Weeks 3-4)
**Goal:** Handle edge cases, retries, checkpointing

**Tasks:**
- [ ] Add retry logic with exponential backoff
- [ ] Implement checkpoint system (resume from last block)
- [ ] Handle chain reorgs
- [ ] Add structured logging
- [ ] Error handling and validation
- [ ] Performance optimization (batch inserts)

**Deliverable:** Runs reliably for 24+ hours without crashes

### Phase 3: Multi-Chain (Weeks 5-6)
**Goal:** Add Base L2 support

**Tasks:**
- [ ] Abstract extractor interface
- [ ] Implement Base L2 extractor
- [ ] Handle L2-specific fields (L1 batch info)
- [ ] Update CLI for chain selection
- [ ] Add chain-specific tests

**Deliverable:** Support both Ethereum and Base

### Phase 4: Polish (Weeks 7-8)
**Goal:** Documentation, examples, packaging

**Tasks:**
- [ ] Write comprehensive README
- [ ] Create example configs
- [ ] Add CLI help text
- [ ] Package for PyPI
- [ ] Create demo video
- [ ] Write launch blog post

**Deliverable:** Ready for open-source launch

---

## Success Metrics

### Technical
- **Sync Speed:** >100 blocks/second (Ethereum)
- **Uptime:** 99.9% (24+ hour runs)
- **Test Coverage:** >80%
- **Type Safety:** 100% (mypy strict)
- **Memory Usage:** <500MB for 1M blocks

### Product
- **GitHub Stars:** 100+ in first month
- **Active Users:** 50+ running in production
- **Chains Supported:** 2+ (Ethereum, Base)
- **Destinations:** 2+ (Postgres, Files)

---

## Learning Resources

### Blockchain Basics
- [Ethereum Whitepaper](https://ethereum.org/en/whitepaper/)
- [How Ethereum Works](https://ethereum.org/en/developers/docs/)
- [Base Documentation](https://docs.base.org/)

### Python Development
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Typer Tutorial](https://typer.tiangolo.com/)
- [pytest Documentation](https://docs.pytest.org/)

### Data Engineering
- [Kimball Dimensional Modeling](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)

---

## Getting Help

**Questions?** Ask in:
- Discord: #chainetl channel (coming soon)
- GitHub Issues: Technical questions
- Direct: Reach out to JT

**Code Reviews:**
- Open PRs early and often
- Tag @jtaylortech for review
- Aim for small, focused PRs (<500 lines)

---

## Related Products

- **ChainWatch** — Monitor your ChainETL pipelines
- **ValidatorHub** — Analyze validator performance with ChainETL data
- **NodeQuick** — Deploy the RPC nodes that ChainETL connects to

---

**Let's build the best blockchain data pipeline tool in the world.**

