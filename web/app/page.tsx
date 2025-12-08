import Link from "next/link";

const products = [
  { name: "ChainOps", desc: "Infrastructure-as-Code for validators", status: "building" },
  { name: "ChainETL", desc: "Blockchain data pipelines", status: "building" },
  { name: "ChainWatch", desc: "Observability for decentralized systems", status: "soon" },
  { name: "SecurityKit", desc: "Automated security for node operators", status: "soon" },
  { name: "DAOForm", desc: "Governance-as-Code", status: "soon" },
];

export default function Home() {
  return (
    <main className="min-h-screen px-6 py-16 md:py-24">
      <div className="max-w-2xl mx-auto">
        {/* Hero */}
        <div className="space-y-4">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight">
            Celara
          </h1>
          <p className="text-lg md:text-xl text-[var(--muted)] leading-relaxed">
            Open-source infrastructure for blockchain validators, node operators, and DAOs. 
            The HashiCorp of Web3.
          </p>
        </div>

        {/* Products */}
        <div className="mt-16 space-y-1">
          {products.map((product) => (
            <div
              key={product.name}
              className="group flex items-center justify-between py-3 border-b border-[var(--border)]"
            >
              <div className="flex items-center gap-4">
                <span className="font-medium">{product.name}</span>
                <span className="text-sm text-[var(--muted)]">{product.desc}</span>
              </div>
              <span className="text-xs text-[var(--muted)] opacity-60">
                {product.status === "building" ? "In development" : "Coming soon"}
              </span>
            </div>
          ))}
        </div>

        {/* Links */}
        <div className="mt-16 flex items-center gap-6 text-sm">
          <Link
            href="https://github.com/jtaylortech/celara-homepage"
            className="text-[var(--accent)] hover:underline underline-offset-4"
          >
            GitHub
          </Link>
          <Link
            href="mailto:jarred@celara.dev"
            className="text-[var(--muted)] hover:text-[var(--text)] transition-colors"
          >
            Contact
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
