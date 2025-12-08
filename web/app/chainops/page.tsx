import Link from "next/link";

export default function ChainOps() {
  return (
    <main className="min-h-screen px-6 py-16 md:py-24">
      <div className="max-w-2xl mx-auto">
        <Link 
          href="/" 
          className="text-sm text-[var(--muted)] hover:text-[var(--text)] transition-colors"
        >
          ← Back
        </Link>

        <div className="mt-8 space-y-4">
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight">
            ChainOps
          </h1>
          <p className="text-[var(--muted)]">
            Infrastructure-as-Code for validators
          </p>
        </div>

        <div className="mt-12 space-y-6 text-[var(--muted)] leading-relaxed">
          <p>
            Deploy blockchain validators with a single command. Terraform and cloud-init 
            templates for Ethereum, Solana, and Cosmos networks.
          </p>
          <p>
            No more manual server setup. No more copy-pasting configs from Discord. 
            Production-grade infrastructure from day one.
          </p>
        </div>

        <div className="mt-12 space-y-3">
          <h2 className="text-sm font-medium text-[var(--text)]">What it does</h2>
          <ul className="space-y-2 text-sm text-[var(--muted)]">
            <li>• One-command validator deployment</li>
            <li>• Multi-chain support (ETH, SOL, Cosmos)</li>
            <li>• Automated security hardening</li>
            <li>• Cost estimation before deploy</li>
            <li>• State tracking across deployments</li>
          </ul>
        </div>

        <div className="mt-12">
          <Link
            href="https://github.com/jtaylortech/celara-homepage/tree/main/chainops"
            className="text-sm text-[var(--accent)] hover:underline underline-offset-4"
          >
            View source →
          </Link>
        </div>
      </div>
    </main>
  );
}
