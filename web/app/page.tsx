import Link from "next/link";

const products = [
  { name: "ChainOps", desc: "Infrastructure-as-Code for validators", status: "dev" },
  { name: "ChainWatch", desc: "Observability for decentralized systems", status: "soon" },
  { name: "ChainETL", desc: "Blockchain data pipelines", status: "dev" },
  { name: "SecurityKit", desc: "Automated security for node operators", status: "soon" },
  { name: "DAOForm", desc: "Governance-as-Code", status: "soon" },
] as const;

const statusLabel = { dev: "In Development", soon: "Coming Soon" } as const;

export default function Home() {
  return (
    <main className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      {/* Hero */}
      <section className="container-celara pt-24 pb-20 sm:pt-32 sm:pb-28">
        <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight">
          Celara
        </h1>
        <p className="mt-4 text-xl sm:text-2xl text-[var(--muted)] max-w-2xl">
          Infrastructure for Decentralized Systems
        </p>
        <p className="mt-6 text-base sm:text-lg text-[var(--muted)] max-w-xl leading-relaxed">
          Open-source primitives that bring DevOps discipline to blockchain validators, node operators, and DAOs.
        </p>
        <div className="mt-10 flex flex-wrap gap-4">
          <Link
            href="https://github.com/celara"
            className="inline-flex h-12 items-center justify-center rounded-lg bg-[var(--accent-1)] px-6 font-medium text-[var(--bg)] transition hover:brightness-105 active:scale-[0.98]"
          >
            View on GitHub
          </Link>
          <Link
            href="#products"
            className="inline-flex h-12 items-center justify-center rounded-lg border border-[var(--border)] px-6 font-medium transition hover:bg-[var(--surface)]"
          >
            Explore Products
          </Link>
        </div>
      </section>

      {/* Products */}
      <section id="products" className="container-celara pb-24 sm:pb-32">
        <h2 className="text-2xl sm:text-3xl font-semibold mb-8">Products</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {products.map((p) => (
            <div
              key={p.name}
              className="rounded-xl border border-[var(--border)] bg-[var(--surface)] p-6 transition hover:border-[var(--accent-1)]/40"
            >
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-semibold">{p.name}</h3>
                <span className="text-xs text-[var(--muted)] bg-[var(--bg)] px-2 py-1 rounded">
                  {statusLabel[p.status]}
                </span>
              </div>
              <p className="text-sm text-[var(--muted)]">{p.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="container-celara pb-12 text-sm text-[var(--muted)]">
        <div className="border-t border-[var(--border)] pt-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <p>2025 Celara. Apache 2.0 License.</p>
          <div className="flex gap-6">
            <Link href="https://github.com/celara" className="hover:text-[var(--text)] transition">
              GitHub
            </Link>
            <Link href="mailto:hello@celara.dev" className="hover:text-[var(--text)] transition">
              Contact
            </Link>
          </div>
        </div>
      </footer>
    </main>
  );
}
