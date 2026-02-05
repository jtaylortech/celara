# ChainETL: In-Depth Technical Documentation

**Last Updated:** February 3, 2026
**Version:** v0.1.0 (Phase 4 - Pre-Launch)
**Author:** Kofi / jtaylortech

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [What Problem Does ChainETL Solve?](#what-problem-does-chainetl-solve)
3. [Architecture Overview](#architecture-overview)
4. [Core Components Deep Dive](#core-components-deep-dive)
5. [Data Flow & Processing](#data-flow--processing)
6. [Multi-Chain Support](#multi-chain-support)
7. [Database Schema & Checkpointing](#database-schema--checkpointing)
8. [Error Handling & Reliability](#error-handling--reliability)
9. [CLI Implementation](#cli-implementation)
10. [Testing Strategy](#testing-strategy)
11. [Performance Characteristics](#performance-characteristics)
12. [Deployment Options](#deployment-options)
13. [Development Phases](#development-phases)
14. [Future Roadmap](#future-roadmap)
15. [Technical Decisions & Trade-offs](#technical-decisions--trade-offs)

---

## Executive Summary

**ChainETL** is a production-grade blockchain data extraction tool that functions as "Airbyte/Fivetran for blockchain data." It automatically extracts data from multiple blockchains (currently Ethereum and Base L2) and loads it into PostgreSQL for analytics and querying.

### Key Stats
- **Test Coverage:** 96%
- **Supported Chains:** 2 (Ethereum, Base L2)
- **Performance:** 50-200 blocks/sec
- **Code Quality:** Strict type checking (mypy), linting (ruff)
- **Production Features:** Checkpointing, reorg detection, retry logic, structured logging

### What Makes It Special
1. **Resumable Syncs** - Never lose progress, pick up where you left off
2. **Multi-Chain** - Independent tracking for multiple blockchains
3. **Type-Safe** - Full type hints with strict mypy validation
4. **Production-Ready** - Retry logic, health checks, Docker support
5. **Simple CLI** - Get started with one command

---

## What Problem Does ChainETL Solve?

### The Challenge

Blockchain data lives on distributed networks and is accessed via RPC (Remote Procedure Call) endpoints. Developers and analysts who want to:
- Analyze historical blockchain data
- Build dashboards and analytics
- Track specific addresses or contracts
- Perform SQL queries on blockchain data

Face these problems:
1. **RPC Limitations** - Rate limits, unreliable connections, slow queries
2. **No Persistence** - Data must be re-fetched every time
3. **Complex Integration** - Writing extraction logic from scratch
4. **No Resumability** - Syncs start over if interrupted
5. **Chain Reorgs** - Blockchains can reorganize, invalidating data

### The Solution

ChainETL solves this by:
1. **Extracting** blockchain data via RPC endpoints
2. **Transforming** raw RPC responses into validated models
3. **Loading** data into PostgreSQL with checkpointing
4. **Resuming** automatically from the last successful block
5. **Detecting** chain reorganizations

Once synced, you can query blockchain data with SQL:
```sql
SELECT
    DATE(timestamp) as date,
    AVG(gas_used) as avg_gas,
    COUNT(*) as blocks
FROM blocks
WHERE number >= 18000000
GROUP BY DATE(timestamp);
```

---

## Architecture Overview

### High-Level Flow

```
┌─────────────┐     ┌────────────┐     ┌──────────┐     ┌────────────┐
│  Blockchain │────▶│ Extractor  │────▶│  Models  │────▶│   Loader   │
│  (via RPC)  │     │ (HTTP GET) │     │(Pydantic)│     │(PostgreSQL)│
└─────────────┘     └────────────┘     └──────────┘     └────────────┘
                           │                                    │
                           │                                    │
                           ▼                                    ▼
                    ┌────────────┐                      ┌────────────┐
                    │ Retry Logic│                      │Checkpoints │
                    │  (exp bo)  │                      │  (resume)  │
                    └────────────┘                      └────────────┘
```

### Layered Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Layer (Typer)                    │
│  - User commands (sync, status)                         │
│  - Progress bars, logging output                        │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│                   Business Logic                        │
│  - Sync orchestration                                   │
│  - Checkpoint management                                │
│  - Reorg detection                                      │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
┌───────▼──────────┐              ┌──────────▼────────┐
│    Extractors    │              │      Loaders      │
│  (Abstract Base) │              │  (Abstract Base)  │
├──────────────────┤              ├───────────────────┤
│ - Ethereum       │              │ - PostgreSQL      │
│ - Base L2        │              │ - (Future: S3)    │
└───────┬──────────┘              └──────────┬────────┘
        │                                    │
┌───────▼──────────┐              ┌──────────▼────────┐
│   RPC Client     │              │   SQLAlchemy      │
│  (httpx + retry) │              │   (ORM + Schema)  │
└──────────────────┘              └───────────────────┘
```

### Component Relationships

```
cli.py
  ├─▶ EthereumExtractor (ethereum.py)
  │     └─▶ RPCClient (rpc.py)
  │           └─▶ retry_with_backoff (retry.py)
  │
  ├─▶ BaseL2Extractor (base_l2.py)
  │     └─▶ RPCClient (rpc.py)
  │
  └─▶ PostgresLoader (postgres.py)
        ├─▶ Block model (block.py)
        ├─▶ Checkpoint model (checkpoint.py)
        └─▶ SQLAlchemy (database ORM)
```

---

## Core Components Deep Dive

### 1. Extractors (`src/chainetl/extractors/`)

**Purpose:** Fetch blockchain data from RPC endpoints

#### Base Extractor (Abstract Interface)
```python
# extractors/base.py
class BaseExtractor(ABC):
    @property
    @abstractmethod
    def chain_name(self) -> str:
        """Name of the blockchain (e.g., 'ethereum', 'base')"""
        pass

    @abstractmethod
    def extract_block(self, block_number: int) -> Block:
        """Extract a single block"""
        pass

    @abstractmethod
    def extract_blocks(self, start: int, end: int) -> list[Block]:
        """Extract multiple blocks (batch)"""
        pass

    @abstractmethod
    def extract_latest_block_number(self) -> int:
        """Get the latest block number from the chain"""
        pass
```

**Design Pattern:** Template Method + Strategy Pattern
- Template provides interface contract
- Implementations provide chain-specific logic

#### Ethereum Extractor
- **File:** `extractors/ethereum.py`
- **RPC Methods Used:**
  - `eth_getBlockByNumber` - Get block data
  - `eth_blockNumber` - Get latest block number
- **Coverage:** 100%
- **Key Features:**
  - Validates block responses with Pydantic
  - Handles missing fields gracefully
  - Batch extraction support

#### Base L2 Extractor
- **File:** `extractors/base_l2.py`
- **Inherits:** Same interface as Ethereum
- **Additional Fields:** L2-specific fields (not yet persisted)
  - `l1BatchNumber` - L1 batch this L2 block belongs to
  - `l1Timestamp` - L1 timestamp reference
  - `sequenceNumber` - Order in L2 sequence
- **Coverage:** 97%

#### RPC Client (`utils/rpc.py`)
```python
class RPCClient:
    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url
        self.client = httpx.Client(timeout=30.0)

    def call(self, method: str, params: list) -> Any:
        """Make RPC call with retry logic"""
        # 1. Build JSON-RPC payload
        # 2. POST to RPC endpoint
        # 3. Handle RPC errors
        # 4. Return result
```

**Features:**
- 30s timeout per request
- Exponential backoff retry (3 attempts)
- RPC error handling
- HTTP error handling
- Coverage: 90%

---

### 2. Models (`src/chainetl/models/`)

**Purpose:** Type-safe data validation using Pydantic

#### Block Model
```python
# models/block.py
class Block(BaseModel):
    number: int                    # Block number (height)
    hash: str                      # Block hash (0x...)
    parent_hash: str               # Previous block hash
    timestamp: int                 # Unix timestamp
    gas_used: int | None = None    # Gas consumed
    gas_limit: int | None = None   # Gas limit
    transactions: list[Transaction] = []  # (future)
```

**Why Pydantic?**
- Automatic validation of RPC responses
- Type coercion (hex strings → integers)
- Clear error messages for invalid data
- JSON serialization built-in

#### Checkpoint Model
```python
# models/checkpoint.py
class Checkpoint(BaseModel):
    chain: str                     # "ethereum", "base"
    last_synced_block: int         # Last successfully synced block
    last_synced_hash: str          # Hash of last synced block
    synced_at: datetime            # When sync completed
    status: str                    # "active", "paused", "failed"
```

**Purpose:** Enable resumable syncs

#### Transaction & Log Models
- **Status:** Defined but not fully utilized yet
- **Future:** Will extract transaction and event log data
- **Coverage:** 100% (validation tests)

---

### 3. Loaders (`src/chainetl/loaders/`)

**Purpose:** Persist extracted data to storage

#### Base Loader (Abstract Interface)
```python
# loaders/base.py
class BaseLoader(ABC):
    @abstractmethod
    def load_block(self, block: Block) -> None:
        """Load a single block"""
        pass

    @abstractmethod
    def load_blocks(self, blocks: list[Block]) -> None:
        """Load multiple blocks"""
        pass

    @abstractmethod
    def save_checkpoint(self, checkpoint: Checkpoint) -> None:
        """Save sync progress"""
        pass

    @abstractmethod
    def load_checkpoint(self, chain: str) -> Checkpoint | None:
        """Load sync progress"""
        pass
```

#### PostgreSQL Loader
- **File:** `loaders/postgres.py`
- **ORM:** SQLAlchemy 2.0+
- **Coverage:** 100%

**Key Methods:**

1. **`load_block(block: Block)`**
   - Insert single block into database
   - Uses `INSERT ... ON CONFLICT DO UPDATE` (upsert)
   - Handles duplicate blocks gracefully

2. **`load_blocks(blocks: list[Block])`**
   - Batch insert for performance
   - Commits entire batch atomically
   - ~10x faster than individual inserts

3. **`save_checkpoint(checkpoint: Checkpoint)`**
   - Upsert checkpoint by chain name
   - Tracks last synced block per chain
   - Enables multi-chain support

4. **`load_checkpoint(chain: str)`**
   - Retrieve last checkpoint for chain
   - Returns `None` if no checkpoint exists
   - Used by `--resume` flag

5. **`detect_reorg(block: Block)`**
   - Checks if `block.parent_hash` matches previous block's hash
   - Returns `True` if chain reorganization detected
   - Logs warning but continues (basic handling)

**Database Schema (SQLAlchemy):**
```python
# Blocks table
class BlockModel(Base):
    __tablename__ = "blocks"
    number = Column(Integer, primary_key=True)
    hash = Column(String, nullable=False, unique=True)
    parent_hash = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)
    gas_used = Column(Integer)
    gas_limit = Column(Integer)

# Checkpoints table
class CheckpointModel(Base):
    __tablename__ = "checkpoints"
    chain = Column(String, primary_key=True)  # PK for multi-chain
    last_synced_block = Column(Integer, nullable=False)
    last_synced_hash = Column(String, nullable=False)
    synced_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
```

---

### 4. Utilities (`src/chainetl/utils/`)

#### Retry Logic (`retry.py`)
```python
@retry_with_backoff(max_attempts=3, base_delay=1.0)
def risky_operation():
    # Will retry up to 3 times with exponential backoff
    # Delays: 1s, 2s, 4s
    pass
```

**Features:**
- Exponential backoff (1s → 2s → 4s)
- Configurable max attempts
- Preserves exception stack traces
- Coverage: 96%

**Use Cases:**
- RPC calls (network flakiness)
- Database operations (transient failures)

---

### 5. CLI (`src/chainetl/cli.py`)

**Framework:** Typer (Click wrapper)
**Coverage:** 97%

#### `chainetl sync` Command

**Signature:**
```bash
chainetl sync \
  --chain ethereum \
  --start-block 18000000 \
  --count 1000 \
  --resume \
  --destination postgres
```

**Parameters:**
- `--chain`: Blockchain to sync (ethereum, base)
- `--start-block`: Starting block number (optional)
- `--destination`: Where to load data (postgres only for now)
- `--resume`: Resume from last checkpoint
- `--count`: Number of blocks to sync (default: 1)

**Logic Flow:**
```python
def sync(...):
    # 1. Initialize extractor (Ethereum or Base)
    extractor = EthereumExtractor(rpc_url) if chain == "ethereum" else ...

    # 2. Initialize loader
    loader = PostgresLoader(database_url)

    # 3. Determine starting block
    if resume:
        checkpoint = loader.load_checkpoint(chain)
        start_block = checkpoint.last_synced_block + 1
    elif start_block is None:
        start_block = extractor.extract_latest_block_number()

    # 4. Extract blocks
    if count == 1:
        block = extractor.extract_block(start_block)
        loader.load_block(block)
    else:
        # Batch extraction
        blocks = extractor.extract_blocks(start_block, start_block + count - 1)
        loader.load_blocks(blocks)

    # 5. Save checkpoint
    checkpoint = Checkpoint(
        chain=chain,
        last_synced_block=blocks[-1].number,
        last_synced_hash=blocks[-1].hash,
        synced_at=datetime.now(UTC),
        status="active"
    )
    loader.save_checkpoint(checkpoint)
```

**Progress Bar (Large Batches):**
- Shown when `count >= 10`
- Uses typer's progressbar
- Shows position and total

#### `chainetl status` Command

**Signature:**
```bash
chainetl status --chain ethereum
```

**Output:**
```
ChainETL Status:
  Chain: ethereum
  Status: Ready
  RPC: https://eth.llamarpc.com
  Database: postgresql://localhost/chainetl

Checkpoint:
  Last synced block: 18000500
  Last synced hash: 0xabc...
  Synced at: 2026-02-03 12:30:00
  Status: active
```

---

## Data Flow & Processing

### Single Block Sync Flow

```
User: chainetl sync --start-block 18000000

    │
    ▼
┌──────────────────────────────────────────┐
│  CLI: Parse arguments                    │
│  chain=ethereum, start_block=18000000    │
└──────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────┐
│  Initialize EthereumExtractor            │
│  rpc_url = settings.ethereum_rpc_url     │
└──────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────┐
│  RPCClient.call(                         │
│    "eth_getBlockByNumber",               │
│    ["0x112a880", true]                   │
│  )                                       │
└──────────────────────────────────────────┘
    │ (retry on failure)
    ▼
┌──────────────────────────────────────────┐
│  RPC Response (JSON):                    │
│  {                                       │
│    "number": "0x112a880",                │
│    "hash": "0xabc...",                   │
│    "parentHash": "0x123...",             │
│    ...                                   │
│  }                                       │
└──────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────┐
│  Pydantic Validation:                    │
│  Block(                                  │
│    number=18000000,  # hex → int         │
│    hash="0xabc...",                      │
│    parent_hash="0x123...",               │
│    ...                                   │
│  )                                       │
└──────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────┐
│  Reorg Detection:                        │
│  loader.detect_reorg(block)              │
│  - Fetch previous block from DB          │
│  - Compare block.parent_hash == prev.hash│
└──────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────┐
│  PostgresLoader.load_block(block)        │
│  INSERT INTO blocks (...) VALUES (...)   │
│  ON CONFLICT (number) DO UPDATE          │
└──────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────┐
│  Save Checkpoint:                        │
│  INSERT INTO checkpoints (...)           │
│  VALUES ("ethereum", 18000000, ...)      │
└──────────────────────────────────────────┘
    │
    ▼
  Success! Block synced.
```

### Batch Sync Flow (count >= 10)

```
User: chainetl sync --start-block 18000000 --count 100

    │
    ▼
  Initialize extractor & loader
    │
    ▼
┌──────────────────────────────────────────┐
│  Progress Bar: [████░░░░░░] 40/100       │
│                                          │
│  Loop through blocks 18000000-18000099:  │
│    - Extract block N                     │
│    - Add to batch                        │
│    - Update progress bar                 │
└──────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────┐
│  Batch Load:                             │
│  loader.load_blocks(blocks)              │
│  - Single transaction                    │
│  - All or nothing (atomicity)            │
└──────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────┐
│  Save Checkpoint (last block only):      │
│  checkpoint.last_synced_block = 18000099 │
└──────────────────────────────────────────┘
```

---

## Multi-Chain Support

### Design Philosophy

**Independent Checkpoints:** Each chain maintains its own checkpoint in the database, allowing:
- Simultaneous syncing of multiple chains
- Chain-specific resume points
- No cross-chain interference

### Implementation

#### 1. Chain Identification
```python
# Checkpoints table uses chain as primary key
checkpoints:
  - chain: "ethereum"  (PK)
    last_synced_block: 18000500

  - chain: "base"      (PK)
    last_synced_block: 10000200
```

#### 2. Extractor Selection
```python
# cli.py
if chain == "ethereum":
    extractor = EthereumExtractor(settings.ethereum_rpc_url)
elif chain == "base":
    extractor = BaseL2Extractor(settings.base_rpc_url)
```

#### 3. Configuration (Environment Variables)
```bash
# .env
ETHEREUM_RPC_URL=https://eth.llamarpc.com
BASE_RPC_URL=https://mainnet.base.org
DATABASE_URL=postgresql://user:pass@localhost/chainetl
```

### Example: Syncing Both Chains

**Terminal 1: Ethereum**
```bash
chainetl sync --chain ethereum --start-block 18000000 --count 1000
```

**Terminal 2: Base L2**
```bash
chainetl sync --chain base --start-block 10000000 --count 2000
```

Both run independently without conflicts!

---

## Database Schema & Checkpointing

### Schema Design

#### Blocks Table
```sql
CREATE TABLE blocks (
    number       INTEGER PRIMARY KEY,     -- Block height
    hash         VARCHAR NOT NULL UNIQUE, -- Block hash
    parent_hash  VARCHAR NOT NULL,        -- Previous block
    timestamp    INTEGER NOT NULL,        -- Unix timestamp
    gas_used     INTEGER,                 -- Gas consumed
    gas_limit    INTEGER,                 -- Max gas allowed

    INDEX idx_timestamp (timestamp),     -- Time-based queries
    INDEX idx_hash (hash)                -- Hash lookups
);
```

**Design Decisions:**
- `number` as PK (natural key, efficient queries)
- `hash` as unique constraint (detect duplicates)
- Indexes on common query patterns

#### Checkpoints Table
```sql
CREATE TABLE checkpoints (
    chain              VARCHAR PRIMARY KEY, -- "ethereum", "base"
    last_synced_block  INTEGER NOT NULL,    -- Resume point
    last_synced_hash   VARCHAR NOT NULL,    -- Verify integrity
    synced_at          TIMESTAMP NOT NULL,  -- Audit trail
    status             VARCHAR NOT NULL     -- "active", "paused"
);
```

**Why Store Hash?**
- Detect chain reorganizations
- Verify database integrity
- Ensure continuity across restarts

### Checkpoint Strategy

#### When Checkpoints Are Saved
1. **After every block** (single sync)
2. **After every batch** (batch sync)
3. **On successful load** (not on extract)

#### Why This Matters
- **Crash Recovery:** If process crashes mid-sync, resume from last checkpoint
- **Idempotency:** Re-running same sync range is safe (upserts)
- **Multi-Chain:** Each chain independently tracked

#### Resume Logic
```python
if resume:
    checkpoint = loader.load_checkpoint(chain)
    if checkpoint:
        start_block = checkpoint.last_synced_block + 1
        print(f"Resuming from block {start_block}")
    else:
        print("No checkpoint found, starting fresh")
        start_block = extractor.extract_latest_block_number()
```

---

## Error Handling & Reliability

### 1. Retry Logic (Network Failures)

**What Gets Retried:**
- RPC calls (`eth_getBlockByNumber`, `eth_blockNumber`)
- HTTP connection errors
- Timeout errors

**Retry Strategy:**
```python
@retry_with_backoff(max_attempts=3, base_delay=1.0)
def call_rpc(method, params):
    # Attempt 1: Immediate
    # Attempt 2: Wait 1s
    # Attempt 3: Wait 2s
    # Fail: Raise exception
```

**Why Exponential Backoff?**
- Gives network time to recover
- Avoids overwhelming failing services
- Standard practice for distributed systems

### 2. Chain Reorganization Detection

**What is a Reorg?**
- Blockchain temporarily accepts two competing chains
- Shorter chain is abandoned, longer chain wins
- Previously "confirmed" blocks become invalid

**Detection Logic:**
```python
def detect_reorg(self, block: Block) -> bool:
    # Get previous block from database
    prev_block = self.get_block_by_number(block.number - 1)

    if not prev_block:
        return False  # No previous block, can't detect

    # Check if current block's parent matches previous block's hash
    if block.parent_hash != prev_block.hash:
        logger.warning("Reorg detected!", block=block.number)
        return True

    return False
```

**Current Handling:**
- Logs warning to user
- Continues with sync (basic handling)
- **Future:** Rollback affected blocks, re-sync

### 3. Data Validation (Pydantic)

**What Gets Validated:**
- Block numbers are integers
- Hashes are strings (hex format)
- Timestamps are valid
- Required fields are present

**Example:**
```python
# RPC returns invalid data
response = {"number": "invalid", "hash": None}

# Pydantic raises ValidationError
Block(**response)  # ❌ Fails fast with clear error
```

**Why This Matters:**
- Fail fast instead of corrupt data
- Clear error messages for debugging
- Type safety throughout application

### 4. Database Transactions

**Batch Loading:**
```python
def load_blocks(self, blocks: list[Block]) -> None:
    with self.session.begin():  # Start transaction
        for block in blocks:
            # Convert to SQLAlchemy model
            block_model = BlockModel(**block.model_dump())
            self.session.merge(block_model)  # Upsert
        # Commit all or rollback on error
```

**Benefits:**
- Atomic batch inserts (all or nothing)
- No partial state in database
- Fast rollback on error

---

## CLI Implementation

### Design Philosophy

**User Experience Principles:**
1. **Simple defaults** - `chainetl sync` just works
2. **Progressive disclosure** - Advanced options available
3. **Clear feedback** - Progress bars, structured output
4. **Fail-safe** - Resumable, no data loss

### Command Structure

```
chainetl
├── sync          Sync blockchain data
└── status        Show sync status
```

### Sync Command Options

| Option | Default | Description |
|--------|---------|-------------|
| `--chain` | `ethereum` | Blockchain to sync |
| `--start-block` | `latest` | Starting block number |
| `--count` | `1` | Number of blocks |
| `--resume` | `False` | Resume from checkpoint |
| `--destination` | `postgres` | Where to load data |

### Output Formats

#### Single Block Sync
```
Starting from block: 18000000
Loaded block 18000000: 0xabc123...
Checkpoint saved at block 18000000
```

#### Batch Sync (< 10 blocks)
```
Starting from block: 18000000
Syncing blocks 18000000 to 18000004 (5 blocks)
Loaded 5 blocks
Checkpoint saved at block 18000004
```

#### Large Batch Sync (>= 10 blocks)
```
Starting from block: 18000000
Syncing blocks 18000000 to 18000099 (100 blocks)
Extracting blocks  [######################] 100/100
Loaded 100 blocks
Checkpoint saved at block 18000099
```

#### Resume Mode
```
Resuming from checkpoint: block 18000099 -> 18000100
Loaded block 18000100: 0xdef456...
Checkpoint saved at block 18000100
```

#### Reorg Warning
```
WARNING: Chain reorganization detected at block 18000050
The new block's parent hash doesn't match the previous block.
Continuing with sync (reorg handling is basic).
```

### Structured Logging

**Format:** JSON logs to stdout (for production monitoring)

```json
{
  "event": "starting_sync",
  "chain": "ethereum",
  "start_block": 18000000,
  "count": 100,
  "timestamp": "2026-02-03T12:00:00Z"
}
```

**Benefits:**
- Machine-readable logs
- Easy integration with log aggregators (Datadog, Splunk)
- Structured querying

---

## Testing Strategy

### Coverage Breakdown

| Component | Coverage | Test Count | Focus Areas |
|-----------|----------|------------|-------------|
| **CLI** | 97% | 16 tests | Commands, error handling |
| **Extractors** | 100% | 11 tests | RPC calls, validation |
| **Loaders** | 100% | 9 tests | Database operations |
| **Models** | 100% | 3 tests | Validation logic |
| **Utils** | 90-96% | 7 tests | Retry, RPC client |
| **Overall** | **96%** | **46 tests** | - |

### Test Categories

#### 1. Unit Tests
**Purpose:** Test individual functions in isolation

**Example:**
```python
def test_block_from_rpc_minimal():
    """Test Block model can parse minimal RPC response"""
    rpc_response = {
        "number": "0x112a880",
        "hash": "0xabc...",
        "parentHash": "0x123...",
        "timestamp": "0x64a8c8b0",
    }

    block = Block(**rpc_response)

    assert block.number == 18000000
    assert block.hash == "0xabc..."
```

#### 2. Integration Tests
**Purpose:** Test components working together

**Example:**
```python
def test_postgres_loader_with_sqlite():
    """Test PostgresLoader with SQLite (in-memory DB)"""
    loader = PostgresLoader("sqlite:///:memory:")

    block = Block(number=1, hash="0xabc", ...)
    loader.load_block(block)

    checkpoint = loader.load_checkpoint("ethereum")
    assert checkpoint.last_synced_block == 1
```

#### 3. CLI Tests (Mocked)
**Purpose:** Test CLI commands without external dependencies

**Strategy:** Monkeypatch classes with fakes
```python
def test_sync_cli_monkeypatched(monkeypatch):
    """Test CLI sync command with fake extractor/loader"""

    class FakeExtractor:
        def extract_block(self, num: int) -> Block:
            return Block(number=num, ...)

    monkeypatch.setattr("chainetl.cli.EthereumExtractor", FakeExtractor)

    result = runner.invoke(app, ["sync", "--start-block", "18000000"])

    assert result.exit_code == 0
    assert "Loaded block 18000000" in result.stdout
```

### Test Tools

- **pytest** - Test runner
- **pytest-cov** - Coverage reporting
- **pytest-mock** - Monkeypatching
- **sqlite** - In-memory database for integration tests
- **Typer CliRunner** - CLI testing

### Running Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=src/chainetl --cov-report=term-missing

# Specific test file
uv run pytest tests/test_cli.py

# Verbose output
uv run pytest -v
```

---

## Performance Characteristics

### Sync Speed

| Chain | Block Time | Sync Speed | Bottleneck |
|-------|-----------|-----------|------------|
| Ethereum | ~12s | 50-100 blocks/sec | RPC rate limits |
| Base L2 | ~2s | 100-200 blocks/sec | RPC rate limits |

**Why These Speeds?**
- Limited by RPC endpoint rate limits
- Network latency (HTTP round-trips)
- Database write speed (minimal impact)

### Memory Usage

**Typical Sync:**
- Single block: ~1KB RAM
- Batch (100 blocks): ~100KB RAM
- Overall process: <100MB RAM

**Why So Low?**
- Minimal data model (blocks only, no txs yet)
- Streaming processing (no large buffers)
- SQLAlchemy connection pooling

### Database Size

**Per Block:**
- ~500 bytes (block metadata only)

**1 Million Blocks:**
- ~500MB disk space

**Full Ethereum History (~19M blocks):**
- ~9.5GB (blocks only)
- ~100GB+ (with transactions & logs)

### Optimization Opportunities

1. **Parallel Extraction**
   - Current: Sequential block extraction
   - Future: Parallel fetching (asyncio)
   - Expected: 5-10x speedup

2. **Batch Size Tuning**
   - Current: User-configurable
   - Future: Auto-tune based on RPC limits
   - Expected: 2x speedup

3. **Caching**
   - Current: None
   - Future: Redis cache for recent blocks
   - Expected: Faster re-syncs

---

## Deployment Options

### 1. Local Development

**Setup:**
```bash
# Clone repo
git clone https://github.com/jtaylortech/celara-homepage.git
cd chainetl

# Install dependencies
uv sync

# Configure
cp .env.example .env
# Edit .env with your RPC URLs

# Run
chainetl sync --chain ethereum --count 100
```

**Use Case:** Development, testing, small syncs

---

### 2. Docker (Single Container)

**Dockerfile:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copy source
COPY . .

# Run
CMD ["uv", "run", "chainetl", "sync"]
```

**Build & Run:**
```bash
docker build -t chainetl .
docker run -e ETHEREUM_RPC_URL=https://... chainetl
```

**Use Case:** Isolated environment, reproducible builds

---

### 3. Docker Compose (Multi-Service)

**docker-compose.yml:**
```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: chainetl
      POSTGRES_USER: chainetl
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data

  chainetl-ethereum:
    build: .
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://chainetl:secret@postgres/chainetl
      ETHEREUM_RPC_URL: https://eth.llamarpc.com
    command: uv run chainetl sync --chain ethereum --resume --count 1000

  chainetl-base:
    build: .
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://chainetl:secret@postgres/chainetl
      BASE_RPC_URL: https://mainnet.base.org
    command: uv run chainetl sync --chain base --resume --count 2000

volumes:
  postgres_data:
```

**Run:**
```bash
docker-compose up -d
```

**Use Case:** Multi-chain syncing, production-like setup

---

### 4. Cloud Deployment (AWS Example)

**Architecture:**
```
┌─────────────┐
│   ECS Task  │
│  (ChainETL) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   RDS       │
│ (PostgreSQL)│
└─────────────┘
```

**Components:**
- **ECS/Fargate:** Run ChainETL container
- **RDS PostgreSQL:** Managed database
- **CloudWatch:** Logs and monitoring
- **Secrets Manager:** Store RPC URLs

**Benefits:**
- Auto-scaling
- Managed backups (RDS)
- High availability
- Monitoring built-in

---

## Development Phases

### Phase 1: Foundation (Weeks 1-2)
**Goal:** Proof of concept

**Completed:**
- ✅ RPC client with retry logic
- ✅ Ethereum extractor
- ✅ PostgreSQL loader
- ✅ Basic CLI (`chainetl sync`)
- ✅ Block model with Pydantic validation

**Outcome:** Can sync single Ethereum blocks

---

### Phase 2: Reliability (Weeks 3-4)
**Goal:** Production-ready single chain

**Completed:**
- ✅ Checkpoint system (resumable syncs)
- ✅ Batch processing (multiple blocks)
- ✅ Reorg detection
- ✅ Comprehensive error handling
- ✅ Test coverage >80%

**Outcome:** Reliable Ethereum syncing with resume

---

### Phase 3: Multi-Chain (Weeks 5-6)
**Goal:** Support multiple blockchains

**Completed:**
- ✅ Abstract extractor interface
- ✅ Base L2 extractor
- ✅ Independent chain checkpoints
- ✅ Multi-chain configuration
- ✅ E2E multi-chain tests

**Outcome:** Can sync Ethereum + Base simultaneously

---

### Phase 4: Polish & Launch (Weeks 7-8) - **CURRENT**
**Goal:** Launch-ready project

**Completed:**
- ✅ Comprehensive documentation (README, examples)
- ✅ Docker & docker-compose setup
- ✅ Progress bars for UX
- ✅ Test coverage 96%
- ✅ Architecture diagrams
- ✅ FAQ & troubleshooting guide
- ✅ Beginner's guide

**In Progress:**
- ⏳ PyPI package publishing
- ⏳ Blog post / announcement
- ⏳ Demo video

**Outcome:** Public launch ready

---

## Future Roadmap

### Short-Term (3-6 months)

#### 1. Transaction & Log Extraction
**Status:** Models defined, extraction not implemented

**Work Required:**
- Parse transaction data from blocks
- Extract event logs
- Persist to new tables (transactions, logs)
- Add indexes for common queries

**Impact:** Enable contract-level analytics

---

#### 2. Additional Chains
**Targets:** Polygon, Arbitrum, Optimism, Solana

**Work Required:**
- Implement new extractors (some EVM-compatible)
- Solana: Different RPC interface
- Test E2E for each chain

**Impact:** Broader blockchain coverage

---

#### 3. Additional Loaders
**Targets:** BigQuery, Snowflake, S3/Parquet

**BigQuery:**
- Better for analytics at scale
- Integration with Google Cloud

**S3/Parquet:**
- Data lake integration
- Cheap storage for historical data

**Impact:** More flexible data destinations

---

### Medium-Term (6-12 months)

#### 4. Real-Time Streaming Mode
**Current:** Batch extraction (historical sync)
**Future:** Subscribe to new blocks as they arrive

**Implementation:**
- WebSocket connection to RPC
- `eth_subscribe` for new blocks
- Stream processing architecture

**Impact:** Near real-time data updates

---

#### 5. dbt Transformation Layer
**Purpose:** Transform raw blockchain data into analytics models

**Example Transformations:**
- Daily active addresses
- Gas price trends
- Contract deployment stats
- DeFi protocol metrics

**Impact:** Analyst-friendly data models

---

#### 6. API Server Mode
**Purpose:** Query blockchain data via REST API

**Endpoints:**
```
GET /blocks/:number
GET /blocks?from=X&to=Y
GET /transactions/:hash
GET /addresses/:address/transactions
```

**Impact:** Enable frontend applications

---

### Long-Term (12+ months)

#### 7. L2-Specific Features
**Currently Deferred:**
- L1 batch number tracking
- Deposit/withdrawal transactions
- Cross-chain message tracking
- L2 gas economics

**Impact:** Complete L2 analytics

---

#### 8. Smart Contract Decoding
**Purpose:** Decode contract calls into human-readable format

**Example:**
```
Raw: 0xa9059cbb000000000000000000000000...
Decoded: transfer(to=0xabc..., amount=100 USDC)
```

**Implementation:**
- ABI storage and parsing
- Event log decoding
- Function call decoding

**Impact:** Contract interaction analytics

---

#### 9. Incremental Materialized Views
**Purpose:** Pre-compute common analytics queries

**Examples:**
- Hourly/daily block stats
- Token balances over time
- Gas usage trends

**Impact:** 100x faster analytics queries

---

## Technical Decisions & Trade-offs

### 1. Why Python?
**Chosen:** Python 3.12+

**Pros:**
- Rich ecosystem (Pydantic, SQLAlchemy, Typer)
- Fast development iteration
- Easy to read and maintain
- Strong type hints (mypy)

**Cons:**
- Slower than Rust/Go
- GIL limits parallel processing

**Alternative Considered:** Rust
- Faster execution
- Harder to develop quickly
- Smaller ecosystem for blockchain tools

**Decision:** Python for MVP, optimize later if needed

---

### 2. Why PostgreSQL?
**Chosen:** PostgreSQL

**Pros:**
- Battle-tested for analytics
- Rich SQL features (CTEs, window functions)
- JSONB support (future: store raw blocks)
- Excellent tooling (pgAdmin, Metabase)

**Cons:**
- Single-server bottleneck (vs. distributed DBs)
- Not optimized for time-series (vs. TimescaleDB)

**Alternative Considered:** BigQuery
- Better for huge scale
- More expensive
- Less flexible for prototyping

**Decision:** Postgres for v1, BigQuery loader for scale

---

### 3. Why Synchronous (not Async)?
**Chosen:** Synchronous Python with httpx

**Pros:**
- Simpler code (no async/await complexity)
- Easier debugging
- Test code simpler

**Cons:**
- Can't parallelize RPC calls
- Lower throughput potential

**Alternative Considered:** asyncio + aiohttp
- 10x faster potential
- Much more complex

**Decision:** Sync for MVP, async in Phase 5

---

### 4. Why Checkpoints (not Idempotent Syncs)?
**Chosen:** Explicit checkpoint table

**Pros:**
- Fast resume (O(1) lookup)
- Clear audit trail
- Multi-chain support

**Cons:**
- Extra table to manage
- Could infer from max(block.number)

**Alternative:** Query `SELECT MAX(number) FROM blocks`
- Simpler (no checkpoint table)
- Slower on large tables
- Can't track per-chain status

**Decision:** Explicit checkpoints for performance + clarity

---

### 5. Why Typer (not Click)?
**Chosen:** Typer

**Pros:**
- Modern (uses type hints)
- Automatic help text from docstrings
- Built on Click (battle-tested)

**Cons:**
- Newer (less mature than Click)

**Decision:** Better DX, worth the trade-off

---

### 6. Why uv (not pip)?
**Chosen:** uv (Astral's package manager)

**Pros:**
- 10-100x faster than pip
- Better dependency resolution
- Modern lock files
- Written in Rust (fast)

**Cons:**
- Newer (less mature)
- Smaller community

**Alternative:** poetry
- More mature
- Slower
- More complex config

**Decision:** Speed + simplicity wins

---

## Key Learnings & Insights

### What Went Well

1. **Test-Driven Development**
   - 96% coverage from the start
   - Caught bugs early
   - Refactoring with confidence

2. **Abstract Interfaces**
   - Easy to add Base L2 (minimal code)
   - Future chains will be even easier
   - Loader swapping trivial

3. **Type Safety**
   - mypy caught many bugs before runtime
   - Better IDE autocomplete
   - Self-documenting code

4. **Checkpointing Early**
   - Resume feature saved hours of re-syncing
   - Critical for production reliability

### Challenges Faced

1. **RPC Rate Limits**
   - Free endpoints throttle aggressively
   - Solution: Paid RPC providers (Alchemy, QuickNode)
   - Future: Retry with backoff + multiple providers

2. **Chain Reorgs**
   - Detected but not fully handled
   - Future: Rollback + re-sync affected blocks

3. **Large Syncs**
   - Syncing full history takes days
   - Solution: Start from recent block, backfill later

4. **Docker Image Size**
   - Python + dependencies = 500MB+
   - Solution: Multi-stage builds, Alpine Linux

### Best Practices Established

1. **Always use type hints** - mypy strict mode
2. **Write tests first** - TDD mindset
3. **Abstract early** - Interfaces for extensibility
4. **Log everything** - Structured JSON logs
5. **Fail fast** - Pydantic validation
6. **Resume everything** - Checkpoints everywhere
7. **Document as you go** - README + docstrings

---

## Conclusion

ChainETL is a **production-ready blockchain ETL tool** that solves real problems:
- ✅ Extracts blockchain data reliably
- ✅ Handles failures gracefully
- ✅ Resumes from interruptions
- ✅ Supports multiple chains
- ✅ Simple to use (one command)

**Current Status:**
- Phase 4 (Polish & Launch) nearly complete
- 96% test coverage
- Ready for public launch
- Blog post pending

**Next Steps:**
1. Publish to PyPI (`pip install chainetl`)
2. Write launch blog post
3. Share on Twitter, Reddit, HN
4. Gather feedback
5. Begin Phase 5 (async + scale)

---

**Questions? Feedback?**
- GitHub: https://github.com/jtaylortech/celara-homepage/chainetl
- Issues: https://github.com/jtaylortech/celara-homepage/issues

**Built with ❤️ by Kofi**
