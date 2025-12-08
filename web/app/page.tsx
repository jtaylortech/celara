import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <div className="max-w-2xl mx-auto px-6 py-24 md:py-32">
        <h1 className="text-4xl md:text-5xl font-semibold tracking-tight">
          Celara
        </h1>
        
        <p className="mt-4 text-lg md:text-xl text-[var(--muted)] leading-relaxed">
          Open-source infrastructure tools for blockchain validators, node operators, and DAOs. The HashiCorp of Web3.
        </p>

        <div className="mt-12 space-y-4">
          <div className="flex items-baseline gap-3">
            <span className="text-[var(--text)]">ChainOps</span>
            <span className="text-sm text-[var(--muted)]">Infrastructure-as-Code</span>
          </div>
          <div className="flex items-baseline gap-3">
            <span className="text-[var(--text)]">ChainETL</span>
            <span className="text-sm text-[var(--muted)]">Data pipelines</span>
          </div>
          <div className="flex items-baseline gap-3">
            <span className="text-[var(--text)]">ChainWatch</span>
            <span className="text-sm text-[var(--muted)]">Observability</span>
          </div>
          <div className="flex items-baseline gap-3">
            <span className="text-[var(--text)]">SecurityKit</span>
            <span className="text-sm text-[var(--muted)]">Automated security</span>
          </div>
          <div className="flex items-baseline gap-3">
            <span className="text-[var(--text)]">DAOForm</span>
            <span className="text-sm text-[var(--muted)]">Governance-as-Code</span>
          </div>
        </div>

        <div className="mt-12 flex gap-4">
          <Link
            href="https://github.com/jtaylortech/celara-homepage"
            className="text-[var(--accent)] hover:underline"
          >
            GitHub
          </Link>
          <Link
            href="mailto:hello@celara.dev"
            className="text-[var(--muted)] hover:text-[var(--text)]"
          >
            Contact
          </Link>
        </div>

        <p className="mt-16 text-sm text-[var(--muted)]">
          2025
        </p>
      </div>
    </div>
  );
}
