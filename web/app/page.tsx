import Link from "next/link";

const products = [
  {
    name: "ChainETL",
    desc: "Blockchain data pipelines",
    status: "live" as const,
    href: "/chainetl",
    gradient: "from-purple-500 to-pink-500",
  },
  {
    name: "ChainOps",
    desc: "Infrastructure-as-Code for validators",
    status: "building" as const,
    href: "/chainops",
    gradient: "from-yellow-400 to-amber-500",
  },
  {
    name: "ChainWatch",
    desc: "Observability for decentralized systems",
    status: "building" as const,
    href: null,
    gradient: "from-blue-500 to-purple-500",
  },
  {
    name: "SecurityKit",
    desc: "Automated security for node operators",
    status: "soon" as const,
    href: null,
    gradient: "from-pink-500 to-amber-500",
  },
  {
    name: "DAOForm",
    desc: "Governance-as-Code",
    status: "soon" as const,
    href: null,
    gradient: "from-teal-400 to-blue-500",
  },
];

const statusLabel = {
  live: "Live",
  building: "In development",
  soon: "Coming soon",
} as const;

const statusColor = {
  live: "text-emerald-400",
  building: "text-amber-400",
  soon: "text-[var(--muted)]",
} as const;

export default function Home() {
  return (
    <main className="min-h-screen px-6 py-20 md:py-32">
      <div className="max-w-2xl mx-auto">
        <div className="space-y-6">
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight">
            Celara
          </h1>
          <p className="text-xl text-[var(--muted)] leading-relaxed max-w-lg">
            Open-source DevOps tooling for decentralized systems.
            Built for validators, node operators, and DAOs.
          </p>
        </div>

        <div className="mt-16 space-y-0.5">
          {products.map((product) => {
            const inner = (
              <div className="flex items-center justify-between py-4">
                <div className="flex items-center gap-3">
                  <div className={`w-1.5 h-1.5 rounded-full bg-gradient-to-r ${product.gradient}`} />
                  <span className="font-medium">{product.name}</span>
                  <span className="text-sm text-[var(--muted)] hidden sm:inline">
                    {product.desc}
                  </span>
                </div>
                <span className={`text-xs font-medium ${statusColor[product.status]}`}>
                  {statusLabel[product.status]}
                </span>
              </div>
            );

            return product.href ? (
              <Link
                key={product.name}
                href={product.href}
                className="block border-b border-[var(--border)] hover:border-[var(--accent)] transition-colors"
              >
                {inner}
              </Link>
            ) : (
              <div
                key={product.name}
                className="border-b border-[var(--border)]"
              >
                {inner}
              </div>
            );
          })}
        </div>

        <div className="mt-16 flex items-center gap-6 text-sm">
          <Link
            href="https://github.com/jtaylortech/celara-homepage"
            className="text-[var(--accent)] hover:underline underline-offset-4"
          >
            GitHub
          </Link>
          <Link
            href="https://github.com/jtaylortech/celara-homepage/tree/main/chainetl"
            className="text-[var(--accent)] hover:underline underline-offset-4"
          >
            ChainETL Docs
          </Link>
        </div>

        <p className="mt-24 text-xs text-[var(--muted)]">
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
