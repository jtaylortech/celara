import Link from "next/link";

const products = [
  { name: "ChainOps", desc: "Infrastructure-as-Code for validators", status: "building", href: "/chainops" },
  { name: "ChainETL", desc: "Blockchain data pipelines", status: "building", href: "/chainetl" },
  { name: "ChainWatch", desc: "Observability for decentralized systems", status: "soon", href: null },
  { name: "SecurityKit", desc: "Automated security for node operators", status: "soon", href: null },
  { name: "DAOForm", desc: "Governance-as-Code", status: "soon", href: null },
];

export default function Home() {
  return (
    <main className="min-h-screen px-6 py-16 md:py-24">
      <div className="max-w-2xl mx-auto">
        {/* Hero */}
        <div className="space-y-5">
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight">
            Celara
          </h1>
          <p className="text-xl md:text-2xl text-[var(--muted)] leading-relaxed">
            Open-source infrastructure for blockchain validators, node operators, and DAOs. 
            DevOps tooling for decentralized systems.
          </p>
        </div>

        {/* Products */}
        <div className="mt-16 space-y-1">
          {products.map((product) => {
            const content = (
              <>
                <div className="flex items-center gap-4">
                  <span className="text-lg font-medium">{product.name}</span>
                  <span className="text-base text-[var(--muted)]">{product.desc}</span>
                </div>
                <span className="text-sm text-[var(--muted)] opacity-60">
                  {product.status === "building" ? "In development" : "Coming soon"}
                </span>
              </>
            );

            if (product.href) {
              return (
                <Link
                  key={product.name}
                  href={product.href}
                  className="group flex items-center justify-between py-3 border-b border-[var(--border)] hover:border-[var(--accent)] transition-colors"
                >
                  {content}
                </Link>
              );
            }

            return (
              <div
                key={product.name}
                className="flex items-center justify-between py-3 border-b border-[var(--border)]"
              >
                {content}
              </div>
            );
          })}
        </div>

        {/* Links */}
        <div className="mt-16 flex items-center gap-6 text-sm">
          <Link
            href="https://github.com/jtaylortech/celara-homepage"
            className="text-[var(--accent)] hover:underline underline-offset-4"
          >
            GitHub
          </Link>
        </div>

        {/* Footer */}
        <p className="mt-24 text-sm text-[var(--muted)]">
          Built by{" "}
          <Link href="https://jtaylor.app" className="hover:text-[var(--text)] transition-colors">
            Jarred
          </Link>
          {" & "}
          <Link href="https://github.com/kofikwarba" className="hover:text-[var(--text)] transition-colors">
            Kofi
          </Link>
        </p>
      </div>
    </main>
  );
}
