import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "REST API Reference | Celara",
  description: "ChainETL REST API — query blockchain data from any EVM chain over HTTP.",
};

const endpoints = [
  {
    method: "GET",
    path: "/",
    desc: "Health check and API info",
    response: `{
  "status": "ok",
  "version": "0.2.0",
  "chains": 4
}`,
  },
  {
    method: "GET",
    path: "/chains",
    desc: "List all supported chains with latest block numbers",
    response: `[
  {
    "chain": "ethereum",
    "latest_block": 19234567,
    "rpc_url": "https://eth.llamarpc.com"
  },
  {
    "chain": "polygon",
    "latest_block": 55000000,
    "rpc_url": "https://polygon-rpc.com"
  }
]`,
  },
  {
    method: "GET",
    path: "/chains/{chain}",
    desc: "Get chain info including latest block number",
    params: [{ name: "chain", type: "string", desc: "Chain name (ethereum, base, polygon, arbitrum)" }],
    response: `{
  "chain": "ethereum",
  "latest_block": 19234567,
  "rpc_url": "https://eth.llamarpc.com"
}`,
  },
  {
    method: "GET",
    path: "/chains/{chain}/blocks/latest",
    desc: "Get the most recent block",
    params: [{ name: "chain", type: "string", desc: "Chain name" }],
    response: `{
  "chain": "ethereum",
  "number": 19234567,
  "hash": "0xabc...def",
  "parent_hash": "0x123...456",
  "timestamp": 1700000000,
  "transaction_count": 142
}`,
  },
  {
    method: "GET",
    path: "/chains/{chain}/blocks/{block_number}",
    desc: "Get a specific block by number",
    params: [
      { name: "chain", type: "string", desc: "Chain name" },
      { name: "block_number", type: "integer", desc: "Block number" },
    ],
    response: `{
  "chain": "ethereum",
  "number": 18000000,
  "hash": "0xabc...def",
  "parent_hash": "0x123...456",
  "timestamp": 1693526400,
  "transaction_count": 98
}`,
  },
  {
    method: "GET",
    path: "/chains/{chain}/blocks/{block_number}/transactions",
    desc: "Get all transactions in a block",
    params: [
      { name: "chain", type: "string", desc: "Chain name" },
      { name: "block_number", type: "integer", desc: "Block number" },
    ],
    response: `[
  {
    "hash": "0xf1a2...b3c4",
    "block_number": 18000000,
    "from_address": "0x1111...1111",
    "to_address": "0x2222...2222",
    "value": "1000000000000000000",
    "gas": 21000,
    "gas_price": 30000000000,
    "transaction_type": 2
  }
]`,
  },
  {
    method: "GET",
    path: "/chains/{chain}/blocks/{block_number}/full",
    desc: "Get a block with all transactions, logs, and token transfers",
    params: [
      { name: "chain", type: "string", desc: "Chain name" },
      { name: "block_number", type: "integer", desc: "Block number" },
    ],
    response: `{
  "chain": "ethereum",
  "number": 18000000,
  "hash": "0xabc...def",
  "parent_hash": "0x123...456",
  "timestamp": 1693526400,
  "transaction_count": 98,
  "transactions": [
    {
      "hash": "0xf1a2...b3c4",
      "block_number": 18000000,
      "from_address": "0x1111...1111",
      "to_address": "0x2222...2222",
      "value": "1000000000000000000",
      "gas": 21000,
      "gas_price": 30000000000,
      "transaction_type": 2
    }
  ],
  "logs_count": 245,
  "token_transfers": [
    {
      "transaction_hash": "0xf1a2...b3c4",
      "log_index": 0,
      "token_address": "0xdAC1...1eC7",
      "token_standard": "ERC-20",
      "from_address": "0x1111...1111",
      "to_address": "0x2222...2222",
      "value": "1000000"
    }
  ]
}`,
  },
];

const methodColor: Record<string, string> = {
  GET: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
};

export default function APIDocs() {
  return (
    <div className="space-y-12">
      <section>
        <h1 className="text-3xl font-bold mb-4">REST API</h1>
        <p className="text-[var(--muted)] leading-relaxed mb-6">
          Query blockchain data from any EVM chain over HTTP. Real-time data from RPC nodes — no database required.
          Auto-generated interactive docs available at <code className="text-emerald-400">/docs</code> (Swagger) and <code className="text-emerald-400">/redoc</code> (ReDoc) when running the server.
        </p>

        <div className="grid md:grid-cols-3 gap-4 mb-8">
          {[
            { label: "Chains", value: "4 EVM" },
            { label: "Auth", value: "None (open)" },
            { label: "Format", value: "JSON" },
          ].map((s) => (
            <div key={s.label} className="rounded-lg border border-[var(--border)] p-4 text-center">
              <div className="text-lg font-bold">{s.value}</div>
              <div className="text-xs text-[var(--muted)]">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-xl font-bold mb-4">Quick Start</h2>
        <Pre code={`# Start the API server
chainetl serve --port 8000

# Or with uvicorn directly
uvicorn chainetl.api:app --host 0.0.0.0 --port 8000`} />
        <div className="mt-4" />
        <Pre code={`# Query the API
curl http://localhost:8000/chains/ethereum/blocks/latest

# Get a specific block with full data
curl http://localhost:8000/chains/ethereum/blocks/18000000/full`} />
      </section>

      <section>
        <h2 className="text-xl font-bold mb-4">Response Headers</h2>
        <p className="text-sm text-[var(--muted)] mb-4">Every response includes:</p>
        <div className="border border-[var(--border)] rounded-lg overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-[var(--bg)]">
                <th className="text-left px-4 py-2 font-medium">Header</th>
                <th className="text-left px-4 py-2 font-medium">Example</th>
                <th className="text-left px-4 py-2 font-medium">Description</th>
              </tr>
            </thead>
            <tbody>
              {[
                ["X-Request-Id", "a1b2c3d4", "Unique request identifier for debugging"],
                ["X-Response-Time", "42.5ms", "Server-side processing time"],
                ["X-Powered-By", "ChainETL", "Service identifier"],
                ["Access-Control-Allow-Origin", "*", "CORS enabled for all origins"],
              ].map((r) => (
                <tr key={r[0]} className="border-t border-[var(--border)]">
                  <td className="px-4 py-2"><code className="text-emerald-400 text-xs">{r[0]}</code></td>
                  <td className="px-4 py-2 text-[var(--muted)]"><code className="text-xs">{r[1]}</code></td>
                  <td className="px-4 py-2 text-[var(--muted)]">{r[2]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section>
        <h2 className="text-xl font-bold mb-2">Endpoints</h2>
        <p className="text-sm text-[var(--muted)] mb-8">Base URL: <code className="text-emerald-400">http://localhost:8000</code></p>

        <div className="space-y-10">
          {endpoints.map((ep) => (
            <div key={ep.path} className="rounded-xl border border-[var(--border)] overflow-hidden">
              {/* Header */}
              <div className="flex items-center gap-3 px-5 py-3 bg-[var(--surface)] border-b border-[var(--border)]">
                <span className={`text-xs font-bold px-2 py-0.5 rounded border ${methodColor[ep.method]}`}>
                  {ep.method}
                </span>
                <code className="text-sm font-mono">{ep.path}</code>
              </div>

              {/* Body */}
              <div className="p-5 space-y-4">
                <p className="text-sm text-[var(--muted)]">{ep.desc}</p>

                {/* Params */}
                {ep.params && (
                  <div>
                    <h4 className="text-xs font-semibold text-[var(--muted)] uppercase tracking-wide mb-2">Parameters</h4>
                    <div className="border border-[var(--border)] rounded-lg overflow-hidden">
                      <table className="w-full text-sm">
                        <tbody>
                          {ep.params.map((p) => (
                            <tr key={p.name} className="border-t border-[var(--border)] first:border-t-0">
                              <td className="px-3 py-2 w-32">
                                <code className="text-emerald-400 text-xs">{p.name}</code>
                              </td>
                              <td className="px-3 py-2 w-20 text-xs text-[var(--muted)]">{p.type}</td>
                              <td className="px-3 py-2 text-xs text-[var(--muted)]">{p.desc}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {/* Response */}
                <div>
                  <h4 className="text-xs font-semibold text-[var(--muted)] uppercase tracking-wide mb-2">Response</h4>
                  <pre className="p-4 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-xs overflow-x-auto">
                    <code className="text-emerald-400">{ep.response}</code>
                  </pre>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-xl font-bold mb-4">Errors</h2>
        <p className="text-sm text-[var(--muted)] mb-4">All errors return structured JSON:</p>
        <Pre code={`// 400 Bad Request — unsupported chain
{
  "error": "unsupported_chain",
  "message": "Chain 'solana' is not supported",
  "supported": ["ethereum", "base", "polygon", "arbitrum"]
}

// 404 Not Found — block doesn't exist
{
  "detail": "Block 999999999999 not found on ethereum"
}`} />
      </section>

      <section>
        <h2 className="text-xl font-bold mb-4">Client Examples</h2>

        <h3 className="text-sm font-semibold mb-2">Python</h3>
        <Pre code={`import httpx

api = "http://localhost:8000"

# Get latest Ethereum block
block = httpx.get(f"{api}/chains/ethereum/blocks/latest").json()
print(f"Block {block['number']}: {block['transaction_count']} txs")

# Get full block with token transfers
full = httpx.get(f"{api}/chains/polygon/blocks/50000000/full").json()
for t in full["token_transfers"]:
    print(f"{t['token_standard']}: {t['from_address'][:10]}... → {t['to_address'][:10]}...")`} />

        <h3 className="text-sm font-semibold mb-2 mt-6">JavaScript</h3>
        <Pre code={`const api = "http://localhost:8000";

// Get latest block
const block = await fetch(\`\${api}/chains/ethereum/blocks/latest\`).then(r => r.json());
console.log(\`Block \${block.number}: \${block.transaction_count} txs\`);

// Get transactions
const txs = await fetch(\`\${api}/chains/ethereum/blocks/18000000/transactions\`).then(r => r.json());
txs.forEach(tx => console.log(\`\${tx.from_address} → \${tx.to_address}: \${tx.value} wei\`));`} />

        <h3 className="text-sm font-semibold mb-2 mt-6">curl</h3>
        <Pre code={`# Latest block
curl -s http://localhost:8000/chains/ethereum/blocks/latest | jq

# Full block with token transfers
curl -s http://localhost:8000/chains/arbitrum/blocks/200000000/full | jq '.token_transfers'

# Check response headers
curl -v http://localhost:8000/chains/ethereum 2>&1 | grep "X-"`} />
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
