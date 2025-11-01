import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowRight, Shield, ServerCog, Database, Network, LineChart, KeyRound, Layers, Globe, GitBranch } from "lucide-react";

const products = [
  {
    name: "NodeQuick",
    tagline: "Provision & manage validators",
    color: "from-[#4C6FFF] to-[#6B3DF4]",
    icon: ServerCog,
    href: "/products/nodequick",
    category: "infrastructure",
  },
  {
    name: "ChainWatch",
    tagline: "Monitor & alert across nodes",
    color: "from-[#6366F1] to-[#6B3DF4]",
    icon: LineChart,
    href: "/products/chainwatch",
    category: "infrastructure",
  },
  {
    name: "ChainETL",
    tagline: "Stream chain data to your cloud",
    color: "from-[#6B3DF4] to-[#9333EA]",
    icon: Database,
    href: "/products/chainetl",
    category: "infrastructure",
  },
  {
    name: "SecurityKit",
    tagline: "Secure programs, keys, and pipelines",
    color: "from-[#F59E0B] to-[#FB7185]",
    icon: KeyRound,
    href: "/products/securitykit",
    category: "security",
  },
  {
    name: "DAOForm",
    tagline: "Governance-as-code (YAML → DAO)",
    color: "from-[#F05AFF] to-[#F59E0B]",
    icon: GitBranch,
    href: "/products/daoform",
    category: "security",
  },
  {
    name: "ValidatorHub",
    tagline: "Operator economics & analytics",
    color: "from-[#14B8A6] to-[#22D3EE]",
    icon: Layers,
    href: "/products/validatorhub",
    category: "security",
  },
  {
    name: "RunNode Cloud",
    tagline: "SaaS control plane for Celara",
    color: "from-[#111827] to-[#374151]",
    icon: Globe,
    href: "/runnode",
    category: "platform",
  },
  {
    name: "Celara Network",
    tagline: "Federated DePIN validator mesh",
    color: "from-[#6B7280] to-[#9CA3AF]",
    icon: Network,
    href: "/network",
    category: "platform",
  },
];

const groups = [
  {
    key: "operations",
    title: "Operations Lifecycle",
    description:
      "Automate provisioning, observability, and data pipelines for validators and RPC nodes.",
    gradient: "from-[#4C6FFF] to-[#6B3DF4]",
    icon: ServerCog,
    includes: ["NodeQuick", "ChainWatch", "ChainETL"],
  },
  {
    key: "security",
    title: "Security & Governance",
    description:
      "Harden keys and software supply chain, define governance as code, and track operator ROI.",
    gradient: "from-[#FB923C] to-[#F05AFF]",
    icon: Shield,
    includes: ["SecurityKit", "DAOForm", "ValidatorHub"],
  },
];

export default function CelaraLanding() {
  return (
    <div className="min-h-screen w-full bg-[radial-gradient(1200px_800px_at_70%_-20%,rgba(75,0,130,0.25),transparent),radial-gradient(900px_600px_at_-10%_10%,rgba(76,111,255,0.25),transparent)] bg-deepspace text-white">
      {/* Nav */}
      <header className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-orbit to-nebula" />
          <span className="font-semibold tracking-wide">Celara</span>
        </div>
        <nav className="hidden items-center gap-6 md:flex">
          <a className="text-sm text-gray-300 hover:text-white" href="/products">Products</a>
          <a className="text-sm text-gray-300 hover:text-white" href="/open">Open Source</a>
          <a className="text-sm text-gray-300 hover:text-white" href="/runnode">RunNode Cloud</a>
          <a className="text-sm text-gray-300 hover:text-white" href="/docs">Docs</a>
        </nav>
        <div className="flex items-center gap-3">
          <Button variant="secondary">GitHub</Button>
          <Button>Launch Cloud</Button>
        </div>
      </header>

      {/* Hero */}
      <section className="mx-auto max-w-7xl px-6 pb-8 pt-8 md:pt-16">
        <div className="max-w-3xl">
          <Badge className="mb-4 bg-white/10 text-white">Infrastructure for Decentralized Systems</Badge>
          <h1 className="text-4xl font-semibold leading-tight md:text-6xl">
            Automate, observe, and secure blockchain operations
          </h1>
          <p className="mt-4 max-w-2xl text-lg text-gray-300">
            Modular, open‑source primitives that professionalize how decentralized systems are built, monitored, and secured.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button>Explore Products<ArrowRight className="ml-2 h-4 w-4"/></Button>
            <Button variant="outline">Read the Docs</Button>
          </div>
        </div>
      </section>

      {/* Lifecycle Panels */}
      <section className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-6 md:grid-cols-2">
        {groups.map((g) => (
          <Card key={g.key} className="overflow-hidden border-white/10 bg-white/5">
            <div className={`h-2 w-full bg-gradient-to-r ${g.gradient}`} />
            <CardContent className="p-6">
              <div className="flex items-center gap-3">
                <g.icon className="h-6 w-6" />
                <h2 className="text-xl font-semibold">{g.title}</h2>
              </div>
              <p className="mt-2 text-gray-300">{g.description}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                {g.includes.map((name) => {
                  const p = products.find((x) => x.name === name)!;
                  const Icon = p.icon;
                  return (
                    <a key={name} href={p.href} className="group">
                      <div className={`flex items-center gap-2 rounded-full bg-gradient-to-r ${p.color} px-3 py-1.5 text-sm font-medium text-white transition hover:scale-[1.02]`}>
                        <Icon className="h-4 w-4" />
                        {p.name}
                      </div>
                    </a>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        ))}
      </section>

      {/* Product Grid */}
      <section className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-6 flex items-end justify-between">
          <h3 className="text-2xl font-semibold">Celara Tools</h3>
          <a href="/products" className="text-sm text-gray-300 hover:text-white">View all</a>
        </div>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {products.map((p) => {
            const Icon = p.icon;
            return (
              <a key={p.name} href={p.href} className="group">
                <Card className="h-full overflow-hidden border-white/10 bg-white/5 transition hover:border-white/20 hover:bg-white/10">
                  <div className={`h-1.5 w-full bg-gradient-to-r ${p.color}`} />
                  <CardContent className="p-5">
                    <div className="flex items-center gap-3">
                      <div className={`rounded-xl bg-gradient-to-r ${p.color} p-2.5`}> 
                        <Icon className="h-5 w-5 text-white" />
                      </div>
                      <div>
                        <div className="text-base font-semibold">{p.name}</div>
                        <div className="text-sm text-gray-300">{p.tagline}</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </a>
            );
          })}
        </div>
      </section>

      {/* Footer */}
      <footer className="mx-auto max-w-7xl px-6 pb-10">
        <div className="h-px w-full bg-white/10" />
        <div className="mt-6 flex flex-col items-start justify-between gap-4 md:flex-row md:items-center">
          <p className="text-sm text-gray-400">© {new Date().getFullYear()} Celara Technologies, LLC</p>
          <div className="flex items-center gap-4 text-sm text-gray-300">
            <a href="/privacy" className="hover:text-white">Privacy</a>
            <a href="/terms" className="hover:text-white">Terms</a>
            <a href="/open" className="hover:text-white">Open Source</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
