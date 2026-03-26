import Link from "next/link";

const products = [
  {
    name: "ChainETL",
    desc: "Blockchain data pipelines",
    detail: "Extract blocks, transactions, and token transfers from 4 EVM chains. PostgreSQL or JSON Lines output.",
    href: "/chainetl",
    gradient: "from-purple-500 to-pink-500",
    cmd: "chainetl sync --chain ethereum --start-block 18000000 --count 10",
  },
  {
    name: "ChainOps",
    desc: "Infrastructure-as-Code for validators",
    detail: "Deploy validators with one command. Terraform templates for Ethereum and Solana with cost estimation.",
    href: "/chainops",
    gradient: "from-yellow-400 to-amber-500",
    cmd: "chainops init ethereum --network mainnet",
  },
  {
    name: "ChainWatch",
    desc: "Observability for decentralized systems",
    detail: "Prometheus metrics exporter for EVM nodes. Grafana dashboards included. Monitor sync, peers, gas.",
    href: "/chainwatch",
    gradient: "from-blue-500 to-purple-500",
    cmd: "chainwatch exporter --chain ethereum --port 9100",
  },
  {
    name: "SecurityKit",
    desc: "Automated security for node operators",
    detail: "Scan nodes for misconfigurations via RPC. 8 security checks. Markdown reports for audits.",
    href: "/securitykit",
    gradient: "from-pink-500 to-amber-500",
    cmd: "securitykit scan --rpc-url https://eth.llamarpc.com",
  },
  {
    name: "DAOForm",
    desc: "Governance-as-Code",
    detail: "Define DAO governance in YAML. Proposals, weighted voting, quorum rules. Version-controlled.",
    href: "/daoform",
    gradient: "from-teal-400 to-blue-500",
    cmd: "daoform init --name MyDAO",
  },
];

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="px-6 pt-24 pb-20 md:pt-36 md:pb-28">
        <div className="max-w-3xl mx-auto">
          <p className="text-sm font-medium text-[var(--accent)] mb-4 tracking-wide uppercase">
            Open Source
          </p>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight leading-[1.1]">
            DevOps tooling for
            <br />
            <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-amber-400 bg-clip-text text-transparent">
              decentralized systems
            </span>
          </h1>
          <p className="mt-6 text-xl text-[var(--muted)] leading-relaxed max-w-xl">
            Five open-source tools for blockchain validators, node operators, and DAOs.
            Deploy, monitor, analyze, secure, and govern — from a single toolkit.
          </p>

          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              href="https://github.com/jtaylortech/celara-homepage"
              className="px-5 py-2.5 bg-white text-black text-sm font-medium rounded-lg hover:bg-gray-200 transition-colors"
            >
              View on GitHub
            </Link>
            <Link
              href="/docs"
              className="px-5 py-2.5 border border-[var(--border)] text-sm font-medium rounded-lg hover:border-[var(--accent)] transition-colors"
            >
              Documentation
            </Link>
          </div>

          {/* Quick install */}
          <div className="mt-10">
            <pre className="inline-block px-5 py-3 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-sm overflow-x-auto">
              <code>
                <span className="text-[var(--muted)]">$</span>{" "}
                <span className="text-emerald-400">pip install chainetl</span>
              </code>
            </pre>
          </div>
        </div>
      </section>

      {/* Products */}
      <section className="px-6 py-20 border-t border-[var(--border)]">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-sm font-medium text-[var(--muted)] uppercase tracking-wide mb-10">
            The Stack
          </h2>
          <div className="space-y-8">
            {products.map((product) => (
              <Link
                key={product.name}
                href={product.href}
                className="group block p-6 -mx-6 rounded-xl hover:bg-[var(--surface)] transition-colors"
              >
                <div className="flex items-start gap-4">
                  <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${product.gradient} mt-2 shrink-0`} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-1">
                      <span className="text-lg font-semibold">{product.name}</span>
                      <span className="text-xs text-[var(--muted)]">{product.desc}</span>
                    </div>
                    <p className="text-sm text-[var(--muted)] mb-3">{product.detail}</p>
                    <code className="text-xs text-emerald-400/80 bg-emerald-400/5 px-2 py-1 rounded">
                      $ {product.cmd}
                    </code>
                  </div>
                  <span className="text-[var(--muted)] opacity-0 group-hover:opacity-100 transition-opacity text-sm">
                    →
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Why Celara */}
      <section className="px-6 py-20 border-t border-[var(--border)]">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-sm font-medium text-[var(--muted)] uppercase tracking-wide mb-10">
            Why Celara
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { title: "Open Source", body: "Apache 2.0. Every tool, every line. No vendor lock-in." },
              { title: "Composable", body: "Each tool works standalone or as part of the suite. Start with one, adopt more as you grow." },
              { title: "Production-Grade", body: "Type-safe Python. 128+ tests. CI on every push. Built by infrastructure engineers." },
            ].map((item) => (
              <div key={item.title}>
                <h3 className="font-semibold mb-2">{item.title}</h3>
                <p className="text-sm text-[var(--muted)] leading-relaxed">{item.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 py-12 border-t border-[var(--border)]">
        <div className="max-w-3xl mx-auto flex items-center justify-between">
          <p className="text-xs text-[var(--muted)]">
            Built by{" "}
            <Link href="https://jtaylor.app" className="hover:text-[var(--text)] transition-colors">
              Jarred
            </Link>
            {" & "}
            <Link href="https://github.com/kofikwarba" className="hover:text-[var(--text)] transition-colors">
              Kofi
            </Link>
          </p>
          <div className="flex gap-4 text-xs">
            <Link href="https://github.com/jtaylortech/celara-homepage" className="text-[var(--muted)] hover:text-[var(--text)] transition-colors">
              GitHub
            </Link>
          </div>
        </div>
      </footer>
    </main>
  );
}
