import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "ChainETL — Blockchain Data Pipelines | Celara",
  description:
    "Extract blockchain data and load it into your data warehouse. Real-time and batch processing for Ethereum, Base, and more.",
};

export default function ChainETL() {
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
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight">
            ChainETL
          </h1>
          <p className="text-lg text-[var(--muted)]">
            Blockchain data pipelines
          </p>
        </div>

        <div className="mt-12 space-y-6 text-lg text-[var(--muted)] leading-relaxed">
          <p>
            Extract blockchain data and load it into your data warehouse. 
            Real-time and batch processing for Ethereum, Base, and more.
          </p>
          <p>
            Stop writing custom indexers. Get clean, typed data in Parquet, 
            JSON, or direct to your database.
          </p>
        </div>

        <div className="mt-12 space-y-3">
          <h2 className="text-sm font-medium text-[var(--text)]">What it does</h2>
          <ul className="space-y-2 text-sm text-[var(--muted)]">
            <li>• Extract blocks, transactions, logs, traces</li>
            <li>• Multi-chain support (Ethereum, Base L2)</li>
            <li>• Output to Parquet, JSON, PostgreSQL</li>
            <li>• Incremental sync with checkpointing</li>
            <li>• Type-safe Python SDK</li>
          </ul>
        </div>

        <div className="mt-12">
          <Link
            href="https://github.com/jtaylortech/celara-homepage/tree/main/chainetl"
            className="text-sm text-[var(--accent)] hover:underline underline-offset-4"
          >
            View source →
          </Link>
        </div>
      </div>
    </main>
  );
}
