export default function ChainETLDocs() {
  return (
    <div className="space-y-16">
      <section>
        <h1 className="text-3xl font-bold mb-4">ChainETL</h1>
        <p className="text-[var(--muted)] leading-relaxed">
          Extract blocks, transactions, logs, and token transfers from any EVM chain. Load into PostgreSQL or JSON Lines. Resumable syncs, reorg detection, and batch processing built in.
        </p>
        <p className="text-[var(--muted)] leading-relaxed mt-2">
          <strong className="text-[var(--text)]">Supported chains:</strong> Ethereum, Base, Polygon, Arbitrum
        </p>
      </section>

      <section id="quick-start">
        <h2 className="text-xl font-bold mb-4">Quick Start</h2>
        <Pre code={`pip install chainetl
cp .env.example .env  # Set RPC URL + database

# Sync 10 Ethereum blocks to Postgres
chainetl sync --chain ethereum --start-block 18000000 --count 10

# Sync to JSON Lines (no database needed)
chainetl sync --chain polygon --start-block 50000000 --count 100 --destination jsonl

# Resume from checkpoint
chainetl sync --chain ethereum --resume --count 1000

# Check status
chainetl status --chain ethereum`} />
      </section>

      <section id="architecture">
        <h2 className="text-xl font-bold mb-4">Architecture</h2>
        <Pre code={`chainetl/
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
│   ├── log.py            # Event logs
│   ├── token_transfer.py # ERC-20/721 transfers
│   └── checkpoint.py     # Sync progress
├── utils/
│   ├── rpc.py            # JSON-RPC client with retry
│   ├── retry.py          # Exponential backoff
│   └── token_parser.py   # ERC-20/721 event detection
└── cli.py                # Typer CLI`} />
      </section>

      <section id="extraction">
        <h2 className="text-xl font-bold mb-4">How Extraction Works</h2>
        <p className="text-sm text-[var(--muted)] leading-relaxed mb-4">
          ChainETL uses the standard Ethereum JSON-RPC interface (<code className="text-emerald-400">eth_getBlockByNumber</code>, <code className="text-emerald-400">eth_getTransactionReceipt</code>, etc.). Since all EVM chains implement the same spec, a single <code className="text-emerald-400">EVMExtractor</code> class handles every chain.
        </p>
        <p className="text-sm text-[var(--muted)] leading-relaxed mb-4">Extraction happens in layers:</p>
        <ol className="text-sm text-[var(--muted)] space-y-1 list-decimal list-inside mb-4">
          <li>Block metadata (number, hash, timestamp, parent hash)</li>
          <li>Transaction data (from, to, value, gas, input data)</li>
          <li>Transaction receipts (logs, gas used, status)</li>
          <li>Token transfers (parsed from ERC-20/ERC-721 Transfer events)</li>
        </ol>
        <h3 className="font-semibold text-sm mb-2 mt-6">Python SDK</h3>
        <Pre code={`from chainetl.extractors.ethereum import EthereumExtractor

extractor = EthereumExtractor(rpc_url="https://eth.llamarpc.com")

# Single block
block = extractor.extract_block(18000000)

# Block with full data (transactions + logs + token transfers)
block, txs, logs, transfers = extractor.extract_block_with_full_data(18000000)
print(f"{len(txs)} transactions, {len(transfers)} token transfers")`} />
      </section>

      <section id="models">
        <h2 className="text-xl font-bold mb-4">Data Models</h2>
        <p className="text-sm text-[var(--muted)] leading-relaxed mb-4">All data is modeled with Pydantic v2:</p>
        <ul className="text-sm text-[var(--muted)] space-y-2">
          <li><strong className="text-[var(--text)]">Block</strong> — number, hash, parent_hash, timestamp, transaction hashes</li>
          <li><strong className="text-[var(--text)]">Transaction</strong> — full EIP-1559 support (maxFeePerGas, maxPriorityFeePerGas), contract creation (to=None), signature (v, r, s)</li>
          <li><strong className="text-[var(--text)]">Log</strong> — address, topics (indexed params), data (non-indexed), log_index</li>
          <li><strong className="text-[var(--text)]">TokenTransfer</strong> — ERC-20 (fungible) and ERC-721 (NFT) parsed from log topics</li>
          <li><strong className="text-[var(--text)]">Checkpoint</strong> — chain, last_synced_block, last_synced_hash, synced_at, status</li>
        </ul>
        <p className="text-sm text-[var(--muted)] mt-4">All models have a <code className="text-emerald-400">from_rpc()</code> classmethod that handles hex→int conversion from raw RPC responses.</p>
      </section>

      <section id="cli">
        <h2 className="text-xl font-bold mb-4">CLI Reference</h2>
        <Table rows={[
          ["chainetl sync --chain ethereum --start-block N --count N", "Sync blocks to destination"],
          ["chainetl sync --destination jsonl", "Output to JSON Lines files"],
          ["chainetl sync --resume --count 1000", "Resume from last checkpoint"],
          ["chainetl status --chain ethereum", "Show sync status + checkpoint"],
          ["chainetl chains", "List supported blockchains"],
        ]} />
      </section>

      <section id="config">
        <h2 className="text-xl font-bold mb-4">Configuration</h2>
        <Pre code={`# .env
ETHEREUM_RPC_URL=https://eth.llamarpc.com
BASE_RPC_URL=https://mainnet.base.org
POLYGON_RPC_URL=https://polygon-rpc.com
ARBITRUM_RPC_URL=https://arb1.arbitrum.io/rpc
DATABASE_URL=postgresql://localhost/chainetl_dev
LOG_LEVEL=INFO`} />
      </section>

      <section id="adding-chains">
        <h2 className="text-xl font-bold mb-4">Adding a New Chain</h2>
        <p className="text-sm text-[var(--muted)] mb-4">Any EVM-compatible chain. Three files to touch:</p>
        <Pre code={`# 1. extractors/optimism.py
from chainetl.extractors.evm import EVMExtractor

class OptimismExtractor(EVMExtractor):
    def __init__(self, rpc_url: str) -> None:
        super().__init__(rpc_url, chain="optimism")

# 2. Add to config.py:
optimism_rpc_url: HttpUrl = HttpUrl("https://mainnet.optimism.io")

# 3. Add to cli.py SUPPORTED_CHAINS:
"optimism": (OptimismExtractor, str(settings.optimism_rpc_url))`} />
      </section>
    </div>
  );
}

function Pre({ code }: { code: string }) {
  return (
    <pre className="p-4 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-sm overflow-x-auto">
      <code className="text-emerald-400">{code}</code>
    </pre>
  );
}

function Table({ rows }: { rows: string[][] }) {
  return (
    <div className="border border-[var(--border)] rounded-lg overflow-hidden">
      <table className="w-full text-sm">
        <thead><tr className="bg-[var(--bg)]"><th className="text-left px-4 py-2 font-medium">Command</th><th className="text-left px-4 py-2 font-medium">Description</th></tr></thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row[0]} className="border-t border-[var(--border)]">
              <td className="px-4 py-2"><code className="text-emerald-400 text-xs">{row[0]}</code></td>
              <td className="px-4 py-2 text-[var(--muted)]">{row[1]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
