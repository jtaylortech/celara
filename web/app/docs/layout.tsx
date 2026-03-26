import Link from "next/link";

const nav = [
  {
    title: "Getting Started",
    links: [
      { href: "/docs", label: "Overview" },
    ],
  },
  {
    title: "ChainETL",
    links: [
      { href: "/docs/chainetl", label: "Introduction" },
      { href: "/docs/chainetl#quick-start", label: "Quick Start" },
      { href: "/docs/chainetl#architecture", label: "Architecture" },
      { href: "/docs/chainetl#extraction", label: "How Extraction Works" },
      { href: "/docs/chainetl#models", label: "Data Models" },
      { href: "/docs/chainetl#cli", label: "CLI Reference" },
      { href: "/docs/chainetl#config", label: "Configuration" },
      { href: "/docs/chainetl#adding-chains", label: "Adding Chains" },
    ],
  },
  {
    title: "ChainOps",
    links: [
      { href: "/docs/chainops", label: "Introduction" },
      { href: "/docs/chainops#quick-start", label: "Quick Start" },
      { href: "/docs/chainops#how-it-works", label: "How It Works" },
      { href: "/docs/chainops#costs", label: "Cost Estimates" },
      { href: "/docs/chainops#cli", label: "CLI Reference" },
    ],
  },
  {
    title: "ChainWatch",
    links: [
      { href: "/docs/chainwatch", label: "Introduction" },
      { href: "/docs/chainwatch#quick-start", label: "Quick Start" },
      { href: "/docs/chainwatch#metrics", label: "Metrics Reference" },
      { href: "/docs/chainwatch#grafana", label: "Grafana Dashboard" },
      { href: "/docs/chainwatch#alerts", label: "Alert Rules" },
      { href: "/docs/chainwatch#cli", label: "CLI Reference" },
    ],
  },
  {
    title: "SecurityKit",
    links: [
      { href: "/docs/securitykit", label: "Introduction" },
      { href: "/docs/securitykit#quick-start", label: "Quick Start" },
      { href: "/docs/securitykit#checks", label: "Security Checks" },
      { href: "/docs/securitykit#reports", label: "Audit Reports" },
      { href: "/docs/securitykit#custom", label: "Custom Checks" },
      { href: "/docs/securitykit#cli", label: "CLI Reference" },
    ],
  },
  {
    title: "DAOForm",
    links: [
      { href: "/docs/daoform", label: "Introduction" },
      { href: "/docs/daoform#quick-start", label: "Quick Start" },
      { href: "/docs/daoform#governance", label: "Governance Model" },
      { href: "/docs/daoform#sdk", label: "Python SDK" },
      { href: "/docs/daoform#storage", label: "Persistence" },
      { href: "/docs/daoform#cli", label: "CLI Reference" },
    ],
  },
];

export default function DocsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <aside className="hidden md:block w-64 shrink-0 border-r border-[var(--border)] bg-[var(--surface)]">
        <div className="sticky top-0 h-screen overflow-y-auto p-6">
          <Link href="/" className="text-lg font-bold block mb-6 hover:text-[var(--accent)] transition-colors">
            Celara
          </Link>
          <nav className="space-y-6">
            {nav.map((section) => (
              <div key={section.title}>
                <h3 className="text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-2">
                  {section.title}
                </h3>
                <ul className="space-y-1">
                  {section.links.map((link) => (
                    <li key={link.href + link.label}>
                      <Link
                        href={link.href}
                        className="block text-sm text-[var(--muted)] hover:text-[var(--text)] py-1 transition-colors"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </nav>
        </div>
      </aside>

      {/* Mobile nav */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-[var(--surface)] border-t border-[var(--border)] z-50 px-4 py-2 flex gap-2 overflow-x-auto">
        {nav.slice(1).map((section) => (
          <Link
            key={section.title}
            href={section.links[0].href}
            className="text-xs text-[var(--muted)] hover:text-[var(--text)] whitespace-nowrap px-2 py-1 rounded bg-[var(--bg)] border border-[var(--border)]"
          >
            {section.title}
          </Link>
        ))}
      </div>

      {/* Content */}
      <main className="flex-1 min-w-0 px-6 md:px-12 py-12 md:py-16 max-w-3xl">
        {children}
      </main>
    </div>
  );
}
