"""
# ChainETL — Beginner's Guide: In-Depth Breakdown

## Table of Contents
1. What is ChainETL?
2. The Problem It Solves
3. How It Works (Architecture)
4. Key Components Explained
5. Data Flow (Step-by-Step)
6. Your Project Structure
7. Current Phase 1 Features
8. Upcoming Phase 2 Features
9. Technology Stack Explained
10. How to Use ChainETL

---

## 1. What is ChainETL?

**Simple Definition:**
ChainETL is a tool that automatically extracts data from blockchain networks (like Ethereum) and stores it in a database where you can analyze it.

**Analogy:**
Think of it like a robot that:
- Watches a blockchain 24/7
- Grabs each new block of data
- Cleans and organizes it
- Stores it in a database
- Lets you search through it

**Why "ChainETL"?**
- **Chain** = Blockchain
- **ETL** = Extract, Transform, Load (data pipeline term)

---

## 2. The Problem It Solves

### Before ChainETL (The Hard Way)
If you want blockchain data, you have to:
- Run a full Ethereum node (costs $$, takes days to sync)
- Learn complex RPC APIs (complicated technical stuff)
- Write custom code to fetch and store data
- Handle errors and crashes yourself
- Maintain everything yourself

### With ChainETL (The Easy Way)
You just run: `chainetl sync --chain ethereum`
And it handles everything automatically!

---

## 3. How It Works (High-Level Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                    CHAINETL PIPELINE                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  STEP 1: EXTRACT          STEP 2: TRANSFORM    STEP 3: LOAD│
│  ────────────────         ───────────────────   ─────────   │
│                                                             │
│  Blockchain ──> RPC Client ──> Block Model ──> Postgres DB │
│  (Ethereum)     (Fetches)       (Validates)     (Stores)   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**What happens at each step:**

### Step 1: EXTRACT
- ChainETL connects to an Ethereum RPC endpoint (a server that speaks blockchain language)
- Says: "Give me block #18000000"
- RPC sends back raw block data (JSON format)

### Step 2: TRANSFORM
- Raw data is messy and hard to use
- ChainETL converts it into Python objects (Block, Transaction, Log)
- Validates the data (checks it's correct format)
- Converts hex numbers to regular numbers, etc.

### Step 3: LOAD
- ChainETL takes the clean data
- Stores it in a Postgres database
- Now you can query it with SQL!

---

## 4. Key Components Explained

### A. RPC Client (`src/chainetl/utils/rpc.py`)
**What:** A tool that talks to the blockchain
**How:** Sends HTTP requests to an RPC endpoint
**Example:**
```python
rpc.call("eth_getBlockByNumber", [hex(18000000), False])
# Returns: Block data from Ethereum
```

### B. Extractors (`src/chainetl/extractors/`)
**What:** Fetches data from the blockchain
**Types:**
- `EthereumExtractor` - Gets Ethereum data
- `BaseExtractor` - Template for other chains

**What it does:**
```python
extractor = EthereumExtractor("https://eth.llamarpc.com")
block = extractor.extract_block(18000000)
# Returns a Block object with all the data
```

### C. Models (`src/chainetl/models/`)
**What:** Python classes that represent blockchain data
**Types:**
- `Block` - Represents a blockchain block
- `Transaction` - Represents a transaction
- `Log` - Represents an event
- `Checkpoint` - Tracks sync progress

**Example:**
```python
block = Block(
    number=18000000,
    hash="0x95b198e...",
    parent_hash="0x123abc...",
    timestamp=1700000000,
    transactions=["0xabc123", "0xdef456"]
)
```

### D. Loaders (`src/chainetl/loaders/`)
**What:** Saves data to a destination
**Types:**
- `PostgresLoader` - Saves to Postgres database
- `FileLoader` - Would save to CSV/Parquet files

**What it does:**
```python
loader = PostgresLoader("postgresql://localhost/chainetl_dev")
loader.load_block(block)
# Now the block is stored in the database!
```

### E. CLI (`src/chainetl/cli.py`)
**What:** Command-line interface (how you control ChainETL)
**Commands:**
- `chainetl sync` - Start syncing blocks
- `chainetl status` - Check what's happening
- `chainetl resume` - Continue from checkpoint (Phase 2)

---

## 5. Data Flow (Step-by-Step Example)

Let's trace what happens when you run: `uv run chainetl sync --chain ethereum --start-block 18000000`

```
┌─ Step 1: Parse Command
│  "Get block 18000000 from Ethereum and save to Postgres"
│
├─ Step 2: Load Config
│  RPC URL: https://eth.llamarpc.com
│  Database: postgresql://localhost/chainetl_dev
│
├─ Step 3: Create Extractor
│  EthereumExtractor connected to RPC
│
├─ Step 4: Create Loader
│  PostgresLoader connected to database
│
├─ Step 5: Extract Block
│  Extractor calls: eth_getBlockByNumber(18000000)
│  RPC returns: Raw JSON data
│
├─ Step 6: Transform Block
│  Block.from_rpc(json_data)
│  Creates Block object with validated data
│
├─ Step 7: Load Block
│  Loader.load_block(block)
│  SQL INSERT into blocks table
│
└─ Step 8: Confirm Success
  Print: "Loaded block 18000000: 0x95b198e..."
```

---

## 6. Your Project Structure

```
chainetl/
│
├── src/chainetl/
│   ├── __init__.py                 # Package marker
│   ├── cli.py                      # Command-line interface
│   ├── config.py                   # Configuration settings
│   │
│   ├── extractors/                 # Data extraction
│   │   ├── base.py                 # Template class
│   │   └── ethereum.py             # Ethereum-specific
│   │
│   ├── loaders/                    # Data storage
│   │   ├── base.py                 # Template class
│   │   └── postgres.py             # Postgres database
│   │
│   ├── models/                     # Data structures
│   │   ├── block.py                # Block data
│   │   ├── transaction.py          # Transaction data
│   │   ├── log.py                  # Event/log data
│   │   └── checkpoint.py           # Sync progress tracker
│   │
│   └── utils/                      # Helper utilities
│       ├── rpc.py                  # RPC client
│       └── retry.py                # Retry logic
│
├── tests/                          # Test files
│   ├── test_cli.py                 # CLI tests
│   ├── test_config.py              # Config tests
│   ├── test_extractors.py          # Extractor tests
│   ├── test_loaders.py             # Loader tests
│   ├── test_models.py              # Model tests
│   ├── test_models_extra.py        # Extra model tests
│   ├── test_retry.py               # Retry tests
│   └── test_rpc.py                 # RPC tests
│
├── pyproject.toml                  # Dependencies list
├── README.md                       # Project description
└── START-HERE.md                   # Quick start guide
```

---

## 7. Current Phase 1 Features (What Works Now)

### ✅ Basic Syncing
```bash
chainetl sync --chain ethereum --start-block 18000000
```
- Extracts a single block from Ethereum
- Stores it in your local Postgres database
- Shows success message with block hash

### ✅ Status Command
```bash
chainetl status
```
- Shows configured RPC endpoint
- Shows database connection string
- Confirms ChainETL is ready to go

### ✅ Data Models
- `Block` model with validation
- `Transaction` model with RPC parsing
- `Log` model for events

### ✅ Error Handling
- Graceful error messages
- Validation of blockchain data
- Detailed logging

---

## 8. Upcoming Phase 2 Features (What's Next)

### 🔄 Retry Logic
If the RPC server is busy or offline:
```
First attempt: FAIL
Wait 1 second...
Second attempt: FAIL
Wait 2 seconds...
Third attempt: SUCCESS!
```
Automatically retries with increasing delays.

### 📍 Checkpoint System
Saves your progress:
```
Block 18000000 ✓ (saved at 12:00 PM)
Block 18000001 ✓ (saved at 12:01 PM)
```
If it crashes, restart from block 18000001 (not 18000000 again).

### 🔗 Reorg Detection
Blockchain sometimes reorganizes (rare but happens):
- Tracks parent hashes to detect when blockchain branches
- Rolls back to the last confirmed block
- Resumes from there

### 📊 Batch Processing
Instead of syncing 1 block at a time:
- Sync 100 blocks at once
- Much faster (100x speed improvement)
- Still reliable

---

## 9. Technology Stack Explained

### Python 3.11+
**What:** Programming language
**Why:** Popular for data engineering, lots of libraries

### Pydantic
**What:** Data validation library
**Why:** Makes sure blockchain data is correct format before storing

### SQLAlchemy
**What:** Database library
**Why:** Easy way to read/write to Postgres from Python

### Typer
**What:** Command-line framework
**Why:** Creates nice CLI commands (chainetl sync, etc.)

### Postgres
**What:** Database
**Why:** Reliable storage for blockchain data

### httpx
**What:** HTTP client
**Why:** Makes requests to RPC servers

### structlog
**What:** Logging library
**Why:** Organized logs with timestamps and context

---

## 10. How to Use ChainETL

### Setup (One Time)
```bash
cd chainetl
uv sync --all-extras          # Install dependencies
createdb chainetl_dev         # Create database
```

### Run ChainETL
```bash
# Sync a single block
uv run chainetl sync --chain ethereum --start-block 18000000

# Check status
uv run chainetl status

# Run tests
uv run pytest
```

### Query Data in Database
```bash
# Connect to Postgres
psql chainetl_dev

# View blocks
SELECT * FROM blocks;

# See your synced block
SELECT number, hash FROM blocks WHERE number = 18000000;
```

---

## 11. The Big Picture: Why This Matters

### Before (Without ChainETL)
- Blockchain data is locked in the blockchain
- Hard to access, hard to analyze
- Every company builds their own tools (wasteful)

### After (With ChainETL)
- Anyone can extract blockchain data easily
- Data is in a database (easy to query)
- Standard tool everyone uses
- Enables analytics, research, DApps

### Real-World Use Cases
1. **Analytics** - Track Ethereum transaction volumes
2. **Research** - Study blockchain patterns
3. **DApps** - Build apps that need blockchain data
4. **Alerts** - Monitor specific addresses or contracts
5. **Dashboards** - Create real-time dashboards

---

## 12. Quick Glossary

| Term | Meaning |
|------|---------|
| **Block** | A bundle of transactions on blockchain |
| **Transaction** | A transfer or action on blockchain |
| **RPC** | Remote Procedure Call (API to talk to blockchain) |
| **Hash** | Unique fingerprint of a block/transaction |
| **Reorg** | Blockchain reorganizes (rare event) |
| **Checkpoint** | Saved progress point |
| **Backoff** | Waiting with increasing delays between retries |
| **Extractor** | Component that gets data |
| **Loader** | Component that stores data |
| **Postgres** | Database system |
| **CLI** | Command-line interface |

---

## Summary

ChainETL is a complete system that:
1. **Connects** to a blockchain (via RPC)
2. **Extracts** data (blocks, transactions)
3. **Validates** and transforms data (Pydantic models)
4. **Stores** data (Postgres database)
5. **Tracks** progress (checkpoints)
6. **Handles errors** (retries, logging)

Your project is at Phase 1 (basic syncing works!) and moving to Phase 2 (reliability, checkpointing, batch processing).

**Next Steps:** Continue Phase 2 implementation for production-grade reliability! 🚀
"""
