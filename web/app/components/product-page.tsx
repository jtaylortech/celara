import Link from "next/link";

interface Feature {
  title: string;
  desc: string;
}

interface ProductPageProps {
  name: string;
  tagline: string;
  gradient: string;
  description: string;
  installCmd: string;
  screenshotSrc: string;
  screenshotAlt: string;
  demoGif?: string;
  features: Feature[];
  stats: { label: string; value: string }[];
  chains?: string[];
  docsHref: string;
  sourceUrl: string;
}

export function ProductPage({
  name,
  tagline,
  gradient,
  description,
  installCmd,
  screenshotSrc,
  screenshotAlt,
  demoGif,
  features,
  stats,
  chains,
  docsHref,
  sourceUrl,
}: ProductPageProps) {
  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="px-6 pt-20 pb-16 md:pt-32 md:pb-24">
        <div className="max-w-3xl mx-auto">
          <Link href="/" className="text-sm text-[var(--muted)] hover:text-[var(--text)] transition-colors">
            ← Celara
          </Link>

          <div className="mt-8 space-y-4">
            <div className="flex items-center gap-3">
              <div className={`w-3 h-3 rounded-full bg-gradient-to-r ${gradient}`} />
              <h1 className="text-4xl md:text-5xl font-bold tracking-tight">{name}</h1>
            </div>
            <p className="text-xl text-[var(--muted)] max-w-lg">{tagline}</p>
          </div>

          <p className="mt-6 text-[var(--muted)] leading-relaxed max-w-xl">{description}</p>

          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              href={docsHref}
              className="px-5 py-2.5 bg-white text-black text-sm font-medium rounded-lg hover:bg-gray-200 transition-colors"
            >
              Read the Docs
            </Link>
            <Link
              href={sourceUrl}
              className="px-5 py-2.5 border border-[var(--border)] text-sm font-medium rounded-lg hover:border-[var(--accent)] transition-colors"
            >
              View Source
            </Link>
          </div>

          {/* Install */}
          <pre className="mt-8 p-4 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-sm overflow-x-auto">
            <code><span className="text-[var(--muted)]">$</span> <span className="text-emerald-400">{installCmd}</span></code>
          </pre>
        </div>
      </section>

      {/* Demo */}
      <section className="px-6 py-16 border-t border-[var(--border)]">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-sm font-medium text-[var(--muted)] uppercase tracking-wide mb-6">See it in action</h2>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={demoGif || screenshotSrc}
            alt={screenshotAlt}
            className="w-full rounded-xl border border-[var(--border)]"
          />
        </div>
      </section>

      {/* Stats */}
      <section className="px-6 py-16 border-t border-[var(--border)]">
        <div className="max-w-3xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((s) => (
              <div key={s.label}>
                <div className="text-2xl font-bold">{s.value}</div>
                <div className="text-sm text-[var(--muted)]">{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Chains */}
      {chains && (
        <section className="px-6 py-16 border-t border-[var(--border)]">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-sm font-medium text-[var(--muted)] uppercase tracking-wide mb-6">Supported Chains</h2>
            <div className="flex flex-wrap gap-3">
              {chains.map((c) => (
                <span key={c} className="px-4 py-2 bg-[var(--surface)] border border-[var(--border)] rounded-full text-sm">{c}</span>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Features */}
      <section className="px-6 py-16 border-t border-[var(--border)]">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-sm font-medium text-[var(--muted)] uppercase tracking-wide mb-10">Features</h2>
          <div className="grid md:grid-cols-2 gap-8">
            {features.map((f) => (
              <div key={f.title}>
                <h3 className="font-semibold mb-1">{f.title}</h3>
                <p className="text-sm text-[var(--muted)] leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="px-6 py-20 border-t border-[var(--border)]">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-2xl font-bold mb-4">Get started in 30 seconds</h2>
          <pre className="inline-block px-6 py-3 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-sm mb-6">
            <code className="text-emerald-400">$ {installCmd}</code>
          </pre>
          <div className="flex justify-center gap-4">
            <Link href={docsHref} className="text-sm text-[var(--accent)] hover:underline underline-offset-4">
              Documentation →
            </Link>
            <Link href={sourceUrl} className="text-sm text-[var(--muted)] hover:text-[var(--text)] transition-colors">
              GitHub →
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
