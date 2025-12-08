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
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      {/* Hero */}
      <section className="min-h-screen flex flex-col justify-center px-6 md:px-12 lg:px-24 py-20">
        <div className="max-w-4xl">
          <h1 className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold tracking-tight leading-[0.95]">
            Celara
          </h1>
          <p className="mt-6 text-xl sm:text-2xl md:text-3xl text-[var(--muted)] max-w-2xl leading-relaxed">
            Infrastructure for Decentralized Systems
          </p>
          
          <div className="mt-12 flex flex-wrap gap-12 md:gap-16">
            <div>
              <div className="text-4xl md:text-5xl font-bold text-[var(--accent-1)]">5</div>
              <div className="text-sm text-[var(--muted)] uppercase tracking-wide mt-1">Products</div>
            </div>
            <div>
              <div className="text-4xl md:text-5xl font-bold text-[var(--accent-1)]">OSS</div>
              <div className="text-sm text-[var(--muted)] uppercase tracking-wide mt-1">Open Source</div>
            </div>
            <div>
              <div className="text-4xl md:text-5xl font-bold text-[var(--accent-1)]">2025</div>
              <div className="text-sm text-[var(--muted)] uppercase tracking-wide mt-1">Launch</div>
            </div>
          </div>

          <div className="mt-12 flex flex-wrap gap-4">
            <Link
              href="https://github.com/jtaylortech/celara-homepage"
              className="inline-flex h-14 items-center justify-center rounded-lg bg-[var(--accent-1)] px-8 font-medium text-[var(--bg)] transition hover:brightness-110"
            >
              View on GitHub
            </Link>
            <Link
              href="#products"
              className="inline-flex h-14 items-center justify-center rounded-lg border border-[var(--border)] px-8 font-medium transition hover:bg-[var(--surface)]"
            >
              Explore Products
            </Link>
          </div>
        </div>
      </section>

      {/* Problem */}
      <section className="px-6 md:px-12 lg:px-24 py-20 border-t border-[var(--border)]">
        <div className="max-w-3xl">
          <h2 className="text-2xl md:text-3xl font-semibold mb-6">The Problem</h2>
          <p className="text-lg md:text-xl text-[var(--muted)] leading-relaxed">
            Blockchain infrastructure today mirrors cloud infrastructure circa 2012 — powerful, chaotic, and highly manual. 
            Every validator, node operator, and DAO builds bespoke tooling. No standards. No interoperability. No DevOps discipline.
          </p>
        </div>
      </section>

      {/* Products */}
      <section id="products" className="px-6 md:px-12 lg:px-24 py-20 border-t border-[var(--border)]">
        <h2 className="text-2xl md:text-3xl font-semibold mb-10">The Stack</h2>
        <div className="grid gap-6 max-w-3xl">
          {products.map((p) => (
            <div key={p.name} className="flex gap-4 items-start">
              <div className="w-3 h-3 rounded-full bg-gradient-to-br from-[var(--accent-1)] to-[var(--accent-2)] mt-2 flex-shrink-0" />
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-1">
                  <h3 className="text-lg font-semibold">{p.name}</h3>
                  <span className="text-xs text-[var(--muted)] bg-[var(--surface)] px-2 py-0.5 rounded">
                    {statusLabel[p.status]}
                  </span>
                </div>
                <p className="text-[var(--muted)]">{p.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Vision */}
      <section className="px-6 md:px-12 lg:px-24 py-20 border-t border-[var(--border)]">
        <div className="max-w-3xl">
          <h2 className="text-2xl md:text-3xl font-semibold mb-6">The Vision</h2>
          <p className="text-lg md:text-xl text-[var(--muted)] leading-relaxed mb-6">
            Modular, open-source primitives that professionalize how decentralized systems are built, monitored, and secured.
          </p>
          <p className="text-xl md:text-2xl font-medium">
            We&apos;re building the HashiCorp of Web3.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 md:px-12 lg:px-24 py-12 border-t border-[var(--border)] text-sm text-[var(--muted)]">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <p>Celara · Apache 2.0 · Built by <Link href="https://jtaylor.app" className="text-[var(--accent-1)] hover:underline">JT</Link></p>
          <div className="flex gap-6">
            <Link href="https://github.com/jtaylortech/celara-homepage" className="hover:text-[var(--text)] transition">GitHub</Link>
            <Link href="mailto:hello@celara.dev" className="hover:text-[var(--text)] transition">Contact</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
