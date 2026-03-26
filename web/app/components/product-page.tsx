import Link from "next/link";

interface CodeExample {
  title: string;
  language: string;
  code: string;
}

interface DocSection {
  heading: string;
  content: string;
}

interface ProductPageProps {
  name: string;
  tagline: string;
  description: string;
  features: string[];
  sourceUrl: string;
  chains?: string[];
  installCmd?: string;
  quickStart: CodeExample[];
  architecture?: string;
  docs: DocSection[];
  cliReference: { command: string; description: string }[];
}

export function ProductPage({
  name,
  tagline,
  description,
  features,
  sourceUrl,
  chains,
  installCmd,
  quickStart,
  architecture,
  docs,
  cliReference,
}: ProductPageProps) {
  return (
    <main className="min-h-screen px-6 py-16 md:py-24">
      <div className="max-w-3xl mx-auto">
        <div className="flex items-center gap-4 mb-8">
          <Link href="/" className="text-sm text-[var(--muted)] hover:text-[var(--text)] transition-colors">
            ← Home
          </Link>
          <Link href="/docs" className="text-sm text-[var(--muted)] hover:text-[var(--text)] transition-colors">
            Docs
          </Link>
        </div>

        {/* Hero */}
        <div className="space-y-4 mb-12">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight">{name}</h1>
          <p className="text-lg text-[var(--muted)]">{tagline}</p>
        </div>

        <p className="text-[var(--muted)] leading-relaxed mb-8">{description}</p>

        {/* Install */}
        {installCmd && (
          <pre className="p-4 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-sm overflow-x-auto mb-12">
            <code className="text-emerald-400">$ {installCmd}</code>
          </pre>
        )}

        {/* Quick Start */}
        <section className="mb-12">
          <h2 className="text-xl font-bold mb-6">Quick Start</h2>
          <div className="space-y-6">
            {quickStart.map((example) => (
              <div key={example.title}>
                <h3 className="text-sm font-medium text-[var(--muted)] mb-2">{example.title}</h3>
                <pre className="p-4 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-sm overflow-x-auto">
                  <code className="text-emerald-400">{example.code}</code>
                </pre>
              </div>
            ))}
          </div>
        </section>

        {/* Chains */}
        {chains && chains.length > 0 && (
          <section className="mb-12">
            <h2 className="text-xl font-bold mb-4">Supported Chains</h2>
            <div className="flex flex-wrap gap-2">
              {chains.map((chain) => (
                <span key={chain} className="px-3 py-1.5 text-sm bg-[var(--surface)] border border-[var(--border)] rounded-full text-[var(--muted)]">
                  {chain}
                </span>
              ))}
            </div>
          </section>
        )}

        {/* Features */}
        <section className="mb-12">
          <h2 className="text-xl font-bold mb-4">Features</h2>
          <ul className="space-y-2 text-sm text-[var(--muted)]">
            {features.map((f) => (
              <li key={f} className="flex gap-2">
                <span className="text-emerald-400 shrink-0">✓</span>
                {f}
              </li>
            ))}
          </ul>
        </section>

        {/* Architecture */}
        {architecture && (
          <section className="mb-12">
            <h2 className="text-xl font-bold mb-4">Architecture</h2>
            <pre className="p-4 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-sm overflow-x-auto text-[var(--muted)]">
              {architecture}
            </pre>
          </section>
        )}

        {/* CLI Reference */}
        <section className="mb-12">
          <h2 className="text-xl font-bold mb-4">CLI Reference</h2>
          <div className="border border-[var(--border)] rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-[var(--surface)]">
                  <th className="text-left px-4 py-2 font-medium">Command</th>
                  <th className="text-left px-4 py-2 font-medium">Description</th>
                </tr>
              </thead>
              <tbody>
                {cliReference.map((cmd) => (
                  <tr key={cmd.command} className="border-t border-[var(--border)]">
                    <td className="px-4 py-2">
                      <code className="text-emerald-400 text-xs">{cmd.command}</code>
                    </td>
                    <td className="px-4 py-2 text-[var(--muted)]">{cmd.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Detailed Docs */}
        <section className="mb-12">
          <h2 className="text-xl font-bold mb-6">Documentation</h2>
          <div className="space-y-8">
            {docs.map((section) => (
              <div key={section.heading}>
                <h3 className="font-semibold mb-3">{section.heading}</h3>
                <div className="text-sm text-[var(--muted)] leading-relaxed whitespace-pre-line">
                  {section.content}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Source */}
        <div className="pt-8 border-t border-[var(--border)]">
          <Link href={sourceUrl} className="text-sm text-[var(--accent)] hover:underline underline-offset-4">
            View source on GitHub →
          </Link>
        </div>
      </div>
    </main>
  );
}
