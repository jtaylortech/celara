import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Documentation | Celara",
  description: "Getting started guides and API reference for all Celara tools.",
};

const docs = [
  {
    product: "ChainETL",
    href: "/chainetl",
    sections: [
      { title: "Quick Start", content: "pip install chainetl && chainetl sync --chain ethereum --start-block 18000000 --count 10" },
      { title: "Supported Chains", content: "Ethereum, Base, Polygon, Arbitrum — any EVM-compatible chain." },
      { title: "Output Formats", content: "PostgreSQL (--destination postgres) or JSON Lines (--destination jsonl) for local analysis with jq, DuckDB, or pandas." },
      { title: "Resume Syncs", content: "chainetl sync --chain ethereum --resume --count 1000 — picks up from last checkpoint automatically." },
      { title: "Adding a Chain", content: "Create a 3-line Python file inheriting from EVMExtractor, add RPC URL to config, register in CLI." },
    ],
  },
  {
    product: "ChainWatch",
    href: "/chainwatch",
    sections: [
      { title: "Quick Start", content: "pip install chainwatch && chainwatch exporter --chain ethereum --port 9100" },
      { title: "Metrics", content: "chainwatch_sync_status, chainwatch_current_block, chainwatch_peer_count, chainwatch_gas_price_gwei — all labeled by chain." },
      { title: "Grafana", content: "Import dashboards/node-health.json into Grafana. Chain selector variable included." },
    ],
  },
  {
    product: "ChainOps",
    href: "/chainops",
    sections: [
      { title: "Quick Start", content: "pip install chainops && chainops init ethereum --network mainnet && chainops deploy --dry-run" },
      { title: "Supported Chains", content: "Ethereum (t3.xlarge, 2TB) and Solana (r6i.2xlarge, 2TB) with AWS Terraform templates." },
      { title: "Cost Estimation", content: "chainops estimate — shows monthly cost breakdown before you deploy." },
    ],
  },
  {
    product: "SecurityKit",
    href: "/securitykit",
    sections: [
      { title: "Quick Start", content: "pip install securitykit && securitykit scan --rpc-url https://eth.llamarpc.com" },
      { title: "Checks", content: "8 checks: RPC reachability, unlocked accounts, admin API, debug API, mining status, peer count, sync status, chain ID." },
      { title: "Reports", content: "securitykit report --rpc-url <url> --output report.md — generates a markdown audit report." },
      { title: "CI Integration", content: "Exit code 1 on failures. Use --output json for machine-readable results." },
    ],
  },
  {
    product: "DAOForm",
    href: "/daoform",
    sections: [
      { title: "Quick Start", content: "pip install daoform && daoform init --name MyDAO && daoform validate" },
      { title: "Governance Config", content: "YAML-based: set quorum (10%), threshold (50%), voting period (7 days), timelock (2 days)." },
      { title: "Python SDK", content: "GovernanceEngine class: create_proposal(), cast_vote(), tally(), resolve(). Full Pydantic models." },
    ],
  },
];

export default function Docs() {
  return (
    <main className="min-h-screen px-6 py-16 md:py-24">
      <div className="max-w-3xl mx-auto">
        <Link href="/" className="text-sm text-[var(--muted)] hover:text-[var(--text)] transition-colors">
          ← Home
        </Link>

        <div className="mt-8 mb-16">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight">Documentation</h1>
          <p className="mt-4 text-lg text-[var(--muted)]">
            Getting started with every Celara tool.
          </p>
        </div>

        <div className="space-y-16">
          {docs.map((doc) => (
            <section key={doc.product} id={doc.product.toLowerCase()}>
              <Link href={doc.href} className="group">
                <h2 className="text-2xl font-bold mb-6 group-hover:text-[var(--accent)] transition-colors">
                  {doc.product} <span className="text-[var(--muted)] text-lg">→</span>
                </h2>
              </Link>
              <div className="space-y-6">
                {doc.sections.map((section) => (
                  <div key={section.title}>
                    <h3 className="text-sm font-semibold text-[var(--text)] mb-2">{section.title}</h3>
                    {section.content.startsWith("pip ") || section.content.startsWith("chainetl") || section.content.startsWith("chainwatch") || section.content.startsWith("chainops") || section.content.startsWith("securitykit") || section.content.startsWith("daoform") ? (
                      <pre className="p-3 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-sm overflow-x-auto">
                        <code className="text-emerald-400">$ {section.content}</code>
                      </pre>
                    ) : (
                      <p className="text-sm text-[var(--muted)] leading-relaxed">{section.content}</p>
                    )}
                  </div>
                ))}
              </div>
            </section>
          ))}
        </div>
      </div>
    </main>
  );
}
