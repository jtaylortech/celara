import Link from "next/link";

const products = [
  { name: "ChainETL", href: "/docs/chainetl", desc: "Blockchain data pipelines — extract, transform, load", gradient: "from-purple-500 to-pink-500" },
  { name: "ChainOps", href: "/docs/chainops", desc: "Infrastructure-as-Code for validators — deploy in one command", gradient: "from-yellow-400 to-amber-500" },
  { name: "ChainWatch", href: "/docs/chainwatch", desc: "Observability — Prometheus metrics + Grafana dashboards", gradient: "from-blue-500 to-purple-500" },
  { name: "SecurityKit", href: "/docs/securitykit", desc: "Security scanning — 8 automated checks via RPC", gradient: "from-pink-500 to-amber-500" },
  { name: "DAOForm", href: "/docs/daoform", desc: "Governance-as-Code — proposals, voting, resolution", gradient: "from-teal-400 to-blue-500" },
];

export default function DocsHome() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Celara Documentation</h1>
      <p className="text-[var(--muted)] mb-8 leading-relaxed">
        Five open-source tools for blockchain infrastructure. Each tool works standalone or as part of the suite.
      </p>

      <pre className="p-4 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-sm mb-12 overflow-x-auto">
        <code className="text-emerald-400">$ pip install chainetl chainops chainwatch securitykit daoform</code>
      </pre>

      <div className="space-y-4">
        {products.map((p) => (
          <Link key={p.name} href={p.href} className="group block p-4 rounded-lg border border-[var(--border)] hover:border-[var(--accent)] transition-colors">
            <div className="flex items-center gap-3 mb-1">
              <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${p.gradient}`} />
              <span className="font-semibold group-hover:text-[var(--accent)] transition-colors">{p.name}</span>
            </div>
            <p className="text-sm text-[var(--muted)] ml-5">{p.desc}</p>
          </Link>
        ))}
      </div>

      <div className="mt-12 pt-8 border-t border-[var(--border)]">
        <h2 className="font-bold mb-4">Common Across All Tools</h2>
        <ul className="space-y-2 text-sm text-[var(--muted)]">
          <li>✓ Python 3.11+ with type hints and mypy strict</li>
          <li>✓ Typer CLI with --help on every command</li>
          <li>✓ Configuration via environment variables or .env files</li>
          <li>✓ Structured logging with structlog</li>
          <li>✓ Apache 2.0 license</li>
        </ul>
      </div>
    </div>
  );
}
