import Link from "next/link";

interface ProductPageProps {
  name: string;
  tagline: string;
  description: string;
  features: string[];
  sourceUrl: string;
  chains?: string[];
  installCmd?: string;
}

export function ProductPage({
  name,
  tagline,
  description,
  features,
  sourceUrl,
  chains,
  installCmd,
}: ProductPageProps) {
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
            {name}
          </h1>
          <p className="text-lg text-[var(--muted)]">{tagline}</p>
        </div>

        <p className="mt-10 text-lg text-[var(--muted)] leading-relaxed">
          {description}
        </p>

        {installCmd && (
          <pre className="mt-8 p-4 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-sm overflow-x-auto">
            <code className="text-emerald-400">$ {installCmd}</code>
          </pre>
        )}

        {chains && chains.length > 0 && (
          <div className="mt-8">
            <h2 className="text-sm font-medium text-[var(--text)] mb-3">
              Supported chains
            </h2>
            <div className="flex flex-wrap gap-2">
              {chains.map((chain) => (
                <span
                  key={chain}
                  className="px-2.5 py-1 text-xs bg-[var(--surface)] border border-[var(--border)] rounded-full text-[var(--muted)]"
                >
                  {chain}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="mt-8">
          <h2 className="text-sm font-medium text-[var(--text)] mb-3">
            Features
          </h2>
          <ul className="space-y-2 text-sm text-[var(--muted)]">
            {features.map((f) => (
              <li key={f}>• {f}</li>
            ))}
          </ul>
        </div>

        <div className="mt-12">
          <Link
            href={sourceUrl}
            className="text-sm text-[var(--accent)] hover:underline underline-offset-4"
          >
            View source →
          </Link>
        </div>
      </div>
    </main>
  );
}
