import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Documentation | Celara",
  description: "Complete documentation for all Celara tools. Quick start guides, CLI reference, architecture, and API docs.",
};

const products = [
  {
    name: "ChainETL",
    href: "/chainetl",
    desc: "Blockchain data pipelines",
    gradient: "from-purple-500 to-pink-500",
    highlights: [
      "Extract blocks, transactions, logs, token transfers from 4 EVM chains",
      "Output to PostgreSQL or JSON Lines",
      "Resumable syncs, reorg detection, batch processing",
      "Python SDK with Pydantic models",
    ],
    cmd: "chainetl sync --chain ethereum --start-block 18000000 --count 10",
  },
  {
    name: "ChainOps",
    href: "/chainops",
    desc: "Infrastructure-as-Code for validators",
    gradient: "from-yellow-400 to-amber-500",
    highlights: [
      "One-command Terraform deployments to AWS",
      "Ethereum and Solana validator templates",
      "Cost estimation before deploy",
      "State tracking and destroy commands",
    ],
    cmd: "chainops init ethereum --network mainnet && chainops deploy",
  },
  {
    name: "ChainWatch",
    href: "/chainwatch",
    desc: "Observability for decentralized systems",
    gradient: "from-blue-500 to-purple-500",
    highlights: [
      "Prometheus metrics exporter for EVM nodes",
      "Sync status, peer count, gas price, client version",
      "Grafana dashboard included (7 panels)",
      "Multi-chain monitoring with chain labels",
    ],
    cmd: "chainwatch exporter --chain ethereum --port 9100",
  },
  {
    name: "SecurityKit",
    href: "/securitykit",
    desc: "Automated security for node operators",
    gradient: "from-pink-500 to-amber-500",
    highlights: [
      "8 RPC-based security checks (no SSH required)",
      "Unlocked accounts, admin API, debug API detection",
      "Markdown audit reports for compliance",
      "JSON output + exit codes for CI/CD",
    ],
    cmd: "securitykit scan --rpc-url https://eth.llamarpc.com",
  },
  {
    name: "DAOForm",
    href: "/daoform",
    desc: "Governance-as-Code",
    gradient: "from-teal-400 to-blue-500",
    highlights: [
      "YAML-based DAO governance configuration",
      "Proposal lifecycle with weighted voting",
      "Quorum and threshold resolution",
      "YAML persistence + Python SDK",
    ],
    cmd: "daoform init --name MyDAO && daoform validate",
  },
];

export default function Docs() {
  return (
    <main className="min-h-screen px-6 py-16 md:py-24">
      <div className="max-w-3xl mx-auto">
        <Link href="/" className="text-sm text-[var(--muted)] hover:text-[var(--text)] transition-colors">
          ← Home
        </Link>

        <div className="mt-8 mb-6">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight">Documentation</h1>
          <p className="mt-4 text-lg text-[var(--muted)]">
            Complete guides for every Celara tool. Click a product for full documentation including architecture, CLI reference, and API docs.
          </p>
        </div>

        {/* Install all */}
        <pre className="p-4 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-sm overflow-x-auto mb-16">
          <code className="text-emerald-400">$ pip install chainetl chainwatch chainops securitykit daoform</code>
        </pre>

        <div className="space-y-12">
          {products.map((product) => (
            <Link
              key={product.name}
              href={product.href}
              className="group block p-6 -mx-6 rounded-xl border border-transparent hover:border-[var(--border)] hover:bg-[var(--surface)] transition-all"
            >
              <div className="flex items-center gap-3 mb-3">
                <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${product.gradient}`} />
                <h2 className="text-xl font-bold group-hover:text-[var(--accent)] transition-colors">
                  {product.name}
                </h2>
                <span className="text-sm text-[var(--muted)]">{product.desc}</span>
                <span className="ml-auto text-[var(--muted)] opacity-0 group-hover:opacity-100 transition-opacity">→</span>
              </div>

              <ul className="space-y-1 mb-4">
                {product.highlights.map((h) => (
                  <li key={h} className="text-sm text-[var(--muted)] flex gap-2">
                    <span className="text-emerald-400/60 shrink-0">✓</span> {h}
                  </li>
                ))}
              </ul>

              <code className="text-xs text-emerald-400/70 bg-emerald-400/5 px-2 py-1 rounded">
                $ {product.cmd}
              </code>
            </Link>
          ))}
        </div>

        {/* Global info */}
        <section className="mt-20 pt-12 border-t border-[var(--border)]">
          <h2 className="text-xl font-bold mb-6">Common Patterns</h2>
          <div className="space-y-6 text-sm text-[var(--muted)] leading-relaxed">
            <div>
              <h3 className="font-semibold text-[var(--text)] mb-2">All tools use the same stack</h3>
              <p>Python 3.11+, Typer CLI, Pydantic models, structlog logging, ruff linting, mypy strict type checking, pytest with coverage. Install any tool with pip or uv.</p>
            </div>
            <div>
              <h3 className="font-semibold text-[var(--text)] mb-2">Configuration via environment variables</h3>
              <p>Every tool reads from environment variables or a .env file. Copy .env.example to .env in any product directory to get started. RPC URLs, database connections, and ports are all configurable.</p>
            </div>
            <div>
              <h3 className="font-semibold text-[var(--text)] mb-2">Adding EVM chains</h3>
              <p>ChainETL, ChainWatch, and SecurityKit all work with any EVM-compatible chain. Adding a new chain is a 3-line Python file — inherit from the base class, set the chain name, register the RPC URL.</p>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
