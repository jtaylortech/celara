import Link from "next/link";

const products = [
  {
    name: "ChainETL",
    desc: "Blockchain data pipelines",
    detail: "Index any EVM chain into Postgres or JSON Lines. Blocks, transactions, logs, and ERC-20/721 token transfers — with resumable syncs and reorg detection.",
    href: "/chainetl",
    gradient: "from-purple-500 to-pink-500",
    cmd: "chainetl sync --chain ethereum --start-block 18000000 --count 10",
  },
  {
    name: "ChainOps",
    desc: "Infrastructure-as-Code for validators",
    detail: "Go from zero to running validator in one command. Terraform templates with chain-specific defaults, cost estimation, and security hardening baked in.",
    href: "/chainops",
    gradient: "from-yellow-400 to-amber-500",
    cmd: "chainops init ethereum --network mainnet",
  },
  {
    name: "ChainWatch",
    desc: "Observability for decentralized systems",
    detail: "Prometheus-native metrics for your nodes. Sync status, peer health, gas prices — all labeled by chain. Grafana dashboard with 7 panels included.",
    href: "/chainwatch",
    gradient: "from-blue-500 to-purple-500",
    cmd: "chainwatch exporter --chain ethereum --port 9100",
  },
  {
    name: "SecurityKit",
    desc: "Automated security for node operators",
    detail: "8 RPC-based security checks — no SSH, no agents. Catches unlocked accounts, exposed admin APIs, and sync issues. CI-ready with JSON output and exit codes.",
    href: "/securitykit",
    gradient: "from-pink-500 to-amber-500",
    cmd: "securitykit scan --rpc-url https://eth.llamarpc.com",
  },
  {
    name: "DAOForm",
    desc: "Governance-as-Code",
    detail: "Your DAO's constitution in a YAML file. Proposals, weighted voting, quorum rules — version-controlled and auditable. Python SDK for building governance UIs.",
    href: "/daoform",
    gradient: "from-teal-400 to-blue-500",
    cmd: "daoform init --name MyDAO",
  },
];

function ProductCard({ product }: { product: typeof products[number] }) {
  return (
    <Link
      href={product.href}
      className="group relative overflow-hidden rounded-xl border border-[var(--border)] hover:border-[var(--accent)] transition-all p-6"
    >
      <div className={`absolute top-0 left-0 right-0 h-1 bg-gradient-to-r ${product.gradient}`} />
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-bold">{product.name}</h3>
        <span className="text-xs text-[var(--muted)] opacity-0 group-hover:opacity-100 transition-opacity">→</span>
      </div>
      <p className="text-xs text-[var(--muted)] uppercase tracking-wide mb-2">{product.desc}</p>
      <p className="text-sm opacity-80 leading-relaxed mb-4">{product.detail}</p>
      <code className="block text-xs text-emerald-400 bg-emerald-400/5 border border-emerald-400/10 px-3 py-2 rounded-lg font-mono">
        $ {product.cmd}
      </code>
    </Link>
  );
}

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
          <div className="mt-10 flex flex-wrap gap-3">
            {[
              { name: "chainetl", color: "text-purple-400" },
              { name: "chainops", color: "text-amber-400" },
              { name: "chainwatch", color: "text-blue-400" },
              { name: "securitykit", color: "text-pink-400" },
              { name: "daoform", color: "text-teal-400" },
            ].map((pkg) => (
              <code
                key={pkg.name}
                className={`text-xs ${pkg.color} bg-[var(--surface)] border border-[var(--border)] px-3 py-1.5 rounded-lg`}
              >
                pip install {pkg.name}
              </code>
            ))}
          </div>
        </div>
      </section>

      {/* Products */}
      <section className="px-6 py-20 border-t border-[var(--border)]">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-sm font-medium text-[var(--muted)] uppercase tracking-wide mb-10">
            The Stack
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {products.slice(0, 3).map((product) => (
              <ProductCard key={product.name} product={product} />
            ))}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 md:max-w-[66.666%] md:mx-auto">
            {products.slice(3).map((product) => (
              <ProductCard key={product.name} product={product} />
            ))}
          </div>
        </div>
      </section>

      {/* Why Celara */}
      <section className="px-6 py-20 border-t border-[var(--border)]">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-sm font-medium text-[var(--muted)] uppercase tracking-wide mb-10">
            Why Celara
          </h2>
          <div className="grid md:grid-cols-3 gap-4">
            {[
              { title: "Open Source", body: "Apache 2.0. Every tool, every line. Fork it, extend it, self-host it. No vendor lock-in, ever.", accent: "bg-purple-500" },
              { title: "Composable", body: "Each tool works standalone. Use ChainETL without ChainOps. Adopt one, then add more as your stack grows.", accent: "bg-blue-500" },
              { title: "Production-Grade", body: "128+ tests across 5 products. Type-safe Python with mypy strict. CI on every push. Built to ship.", accent: "bg-emerald-500" },
            ].map((item) => (
              <div key={item.title} className="rounded-xl border border-[var(--border)] p-6">
                <div className={`w-8 h-1 ${item.accent} rounded-full mb-4`} />
                <h3 className="font-bold mb-2">{item.title}</h3>
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
