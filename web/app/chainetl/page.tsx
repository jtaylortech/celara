import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "ChainETL — Blockchain Data Pipelines | Celara",
  description: "Extract blockchain data from EVM chains into PostgreSQL or JSON Lines. Multi-chain, resumable, type-safe.",
};

export default function ChainETL() {
  return (
    <ProductPage
      name="ChainETL"
      tagline="Blockchain data pipelines"
      description="Extract blocks, transactions, logs, and token transfers from any EVM chain. Load into PostgreSQL for analytics or JSON Lines for local processing. Resumable syncs with checkpointing, chain reorganization detection, and ERC-20/ERC-721 token transfer parsing. Built with Pydantic models, structured logging, and exponential backoff retry logic."
      installCmd="pip install chainetl"
      chains={["Ethereum", "Base", "Polygon", "Arbitrum"]}
      features={[
        "Multi-chain extraction — 4 EVM chains from a single codebase",
        "PostgreSQL and JSON Lines output formats",
        "Resumable syncs with automatic checkpointing",
        "Chain reorganization (reorg) detection",
        "Full transaction extraction (legacy + EIP-1559)",
        "ERC-20 and ERC-721 token transfer parsing from logs",
        "Batch processing with progress bars for large syncs",
        "Graceful shutdown on SIGTERM/SIGINT",
        "Type-safe Pydantic models for all blockchain data",
        "Structured logging with structlog",
        "Exponential backoff retry on RPC failures",
      ]}
      quickStart={[
        {
          title: "Install and sync 10 Ethereum blocks",
          language: "bash",
          code: `pip install chainetl
cp .env.example .env  # Set your RPC URL + database

chainetl sync --chain ethereum --start-block 18000000 --count 10`,
        },
        {
          title: "Sync to JSON Lines (no database required)",
          language: "bash",
          code: `chainetl sync --chain polygon --start-block 50000000 --count 100 --destination jsonl

# Output: output/polygon_blocks.jsonl
# Each line is a valid JSON object — works with jq, DuckDB, pandas
cat output/polygon_blocks.jsonl | jq '.number'`,
        },
        {
          title: "Resume from last checkpoint",
          language: "bash",
          code: `# First sync stops at block 18000099
chainetl sync --chain ethereum --start-block 18000000 --count 100

# Resume picks up at 18000100 automatically
chainetl sync --chain ethereum --resume --count 1000`,
        },
        {
          title: "Python SDK usage",
          language: "python",
          code: `from chainetl.extractors.ethereum import EthereumExtractor

extractor = EthereumExtractor(rpc_url="https://eth.llamarpc.com")

# Extract a single block
block = extractor.extract_block(18000000)
print(f"Block {block.number}: {len(block.transactions)} txs")

# Extract with full transaction + log + token transfer data
block, txs, logs, transfers = extractor.extract_block_with_full_data(18000000)
print(f"Found {len(transfers)} token transfers")`,
        },
      ]}
      architecture={`chainetl/
├── extractors/           # Chain-specific data extraction
│   ├── evm.py            # Unified EVM extractor (shared by all chains)
│   ├── ethereum.py       # Ethereum (thin wrapper)
│   ├── base_l2.py        # Base L2 (thin wrapper)
│   ├── polygon.py        # Polygon (thin wrapper)
│   └── arbitrum.py       # Arbitrum (thin wrapper)
├── loaders/              # Output destinations
│   ├── postgres.py       # PostgreSQL via SQLAlchemy
│   └── jsonl.py          # JSON Lines file output
├── models/               # Pydantic data models
│   ├── block.py          # Block (number, hash, timestamp, txs)
│   ├── transaction.py    # Transaction (legacy + EIP-1559)
│   ├── log.py            # Event logs (address, topics, data)
│   ├── token_transfer.py # ERC-20/721 transfers
│   └── checkpoint.py     # Sync progress tracking
├── utils/
│   ├── rpc.py            # JSON-RPC client with retry
│   ├── retry.py          # Exponential backoff
│   └── token_parser.py   # ERC-20/721 event detection
└── cli.py                # Typer CLI (sync, status, chains)`}
      cliReference={[
        { command: "chainetl sync --chain ethereum --start-block 18000000 --count 10", description: "Sync blocks from a chain to destination" },
        { command: "chainetl sync --chain polygon --destination jsonl", description: "Sync to JSON Lines files instead of Postgres" },
        { command: "chainetl sync --chain ethereum --resume --count 1000", description: "Resume from last checkpoint" },
        { command: "chainetl status --chain ethereum", description: "Show sync status and checkpoint info" },
        { command: "chainetl chains", description: "List all supported blockchains" },
      ]}
      docs={[
        {
          heading: "How Extraction Works",
          content: `ChainETL uses the standard Ethereum JSON-RPC interface (eth_getBlockByNumber, eth_getTransactionReceipt, etc.) to extract data. Since all EVM chains implement the same RPC spec, a single EVMExtractor class handles Ethereum, Base, Polygon, and Arbitrum.

Each chain-specific extractor is a 3-line wrapper that sets the chain name. Adding a new EVM chain is trivial — create a file, inherit from EVMExtractor, register in the CLI.

Extraction happens in layers:
1. Block metadata (number, hash, timestamp, parent hash)
2. Transaction data (from, to, value, gas, input data)
3. Transaction receipts (logs, gas used, status)
4. Token transfers (parsed from ERC-20/ERC-721 Transfer events)`,
        },
        {
          heading: "Data Models",
          content: `All data is modeled with Pydantic v2 for type safety and validation:

• Block: number, hash, parent_hash, timestamp, transaction hashes
• Transaction: full EIP-1559 support (maxFeePerGas, maxPriorityFeePerGas), contract creation detection (to=None), signature fields (v, r, s)
• Log: address, topics (indexed params), data (non-indexed), log_index
• TokenTransfer: ERC-20 (fungible) and ERC-721 (NFT) transfers parsed from log topics
• Checkpoint: chain, last_synced_block, last_synced_hash, synced_at, status

All models have a from_rpc() classmethod that handles hex-to-int conversion from raw RPC responses.`,
        },
        {
          heading: "Reorg Detection",
          content: `Chain reorganizations happen when the network switches to a different fork. ChainETL detects this by comparing the parent_hash of each new block against the hash of the previous block in the database.

If a mismatch is found, ChainETL logs a warning and continues syncing. The new block overwrites the old one (upsert via SQLAlchemy merge). For production use, you may want to implement deeper reorg handling (re-syncing N blocks back).`,
        },
        {
          heading: "Adding a New Chain",
          content: `Any EVM-compatible chain works. Three steps:

1. Create extractors/mychain.py:
   from chainetl.extractors.evm import EVMExtractor
   class MyChainExtractor(EVMExtractor):
       def __init__(self, rpc_url: str) -> None:
           super().__init__(rpc_url, chain="mychain")

2. Add RPC URL to config.py:
   mychain_rpc_url: HttpUrl = HttpUrl("https://rpc.mychain.com")

3. Register in cli.py SUPPORTED_CHAINS dict:
   "mychain": (MyChainExtractor, str(settings.mychain_rpc_url))`,
        },
        {
          heading: "Configuration",
          content: `Environment variables (or .env file):

ETHEREUM_RPC_URL — Ethereum RPC endpoint (default: https://eth.llamarpc.com)
BASE_RPC_URL — Base L2 RPC endpoint (default: https://mainnet.base.org)
POLYGON_RPC_URL — Polygon RPC endpoint (default: https://polygon-rpc.com)
ARBITRUM_RPC_URL — Arbitrum RPC endpoint (default: https://arb1.arbitrum.io/rpc)
DATABASE_URL — PostgreSQL connection string (default: postgresql://localhost/chainetl_dev)
LOG_LEVEL — Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)`,
        },
      ]}
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/chainetl"
    />
  );
}
