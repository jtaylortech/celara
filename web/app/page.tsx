import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowRight, Shield, ServerCog, Database, Network, LineChart, KeyRound, Layers, Globe, GitBranch, Boxes } from "lucide-react";

const products = [
  {
    name: "NodeQuick",
    tagline: "Infrastructure-as-Code for validators",
    color: "from-[#4C6FFF] to-[#6B3DF4]",
    icon: ServerCog,
    href: "/products/nodequick",
  },
  {
    name: "ChainWatch",
    tagline: "Observability for decentralized systems",
    color: "from-[#6366F1] to-[#6B3DF4]",
    icon: LineChart,
    href: "/products/chainwatch",
  },
  {
    name: "ChainETL",
    tagline: "Blockchain data pipelines",
    color: "from-[#6B3DF4] to-[#9333EA]",
    icon: Database,
    href: "/products/chainetl",
  },
  {
    name: "SecurityKit",
    tagline: "Automated security for smart contracts",
    color: "from-[#F59E0B] to-[#FB7185]",
    icon: KeyRound,
    href: "/products/securitykit",
  },
  {
    name: "DAOForm",
    tagline: "Governance-as-Code",
    color: "from-[#F05AFF] to-[#F59E0B]",
    icon: GitBranch,
    href: "/products/daoform",
  },
  {
    name: "ValidatorHub",
    tagline: "Operator economics dashboard",
    color: "from-[#14B8A6] to-[#22D3EE]",
    icon: Layers,
    href: "/products/validatorhub",
  },
  {
    name: "RunNode Cloud",
    tagline: "Managed control plane",
    color: "from-[#6B7280] to-[#9CA3AF]",
    icon: Globe,
    href: "/runnode",
  },
  {
    name: "Celara Network",
    tagline: "Federated validator mesh",
    color: "from-[#4C6FFF] to-[#2DD4BF]",
    icon: Network,
    href: "/network",
  },
];

const pillars = [
  {
    key: "infrastructure",
    title: "Infrastructure",
    description: "Provision, monitor, and scale blockchain infrastructure.",
    icon: Boxes,
    gradient: "from-[#4C6FFF] to-[#6B3DF4]",
  },
  {
    key: "security",
    title: "Security",
    description: "Automated security checks and governance-as-code.",
    icon: Shield,
    gradient: "from-[#FB923C] to-[#F05AFF]",
  },
  {
    key: "platform",
    title: "Platform",
    description: "Managed services for enterprise validator operations.",
    icon: Globe,
    gradient: "from-[#2DD4BF] to-[#4C6FFF]",
  },
];

export default function CelaraLanding() {
  return (
    <div className="min-h-screen w-full bg-black text-white">
      {/* Nav */}
      <header className="fixed top-0 z-50 w-full border-b border-white/5 bg-black/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3">
          <div className="flex items-center gap-2.5">
            <div className="h-7 w-7 rounded-lg bg-gradient-to-tr from-orbit to-nebula" />
            <span className="text-base font-semibold tracking-tight">Celara</span>
          </div>
          <nav className="hidden items-center gap-6 md:flex">
            <a className="text-sm text-gray-400 transition hover:text-white" href="#products">Products</a>
            <a className="text-sm text-gray-400 transition hover:text-white" href="/docs">Docs</a>
            <a className="text-sm text-gray-400 transition hover:text-white" href="/open">GitHub</a>
          </nav>
          <Button size="sm" className="bg-gradient-to-r from-orbit to-plasma">Launch Cloud</Button>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden pt-24 pb-12">
        <div className="absolute top-0 left-1/4 h-96 w-96 rounded-full bg-orbit/20 blur-3xl" />
        <div className="absolute top-20 right-1/4 h-96 w-96 rounded-full bg-nebula/20 blur-3xl" />
        
        <div className="relative mx-auto max-w-6xl px-6 text-center">
          <Badge className="mb-4 border-white/10 bg-white/5 text-xs backdrop-blur-sm">
            Infrastructure for Decentralized Systems
          </Badge>
          <h1 className="mx-auto max-w-4xl text-5xl font-bold leading-[1.1] tracking-tight md:text-6xl lg:text-7xl">
            Build, secure, and operate{" "}
            <span className="bg-gradient-to-r from-orbit via-plasma to-nebula bg-clip-text text-transparent">
              blockchain infrastructure
            </span>
          </h1>
          <p className="mx-auto mt-5 max-w-2xl text-base text-gray-300 md:text-lg">
            Open-source primitives for validators, RPCs, and DAOs. From deployment to monitoring to governance.
          </p>
          <div className="mt-7 flex flex-wrap items-center justify-center gap-3">
            <Button className="bg-gradient-to-r from-orbit to-plasma">
              Explore Products
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button variant="outline" className="border-white/20 bg-transparent hover:bg-white/5">
              Documentation
            </Button>
          </div>
        </div>
      </section>

      {/* Pillars */}
      <section className="py-12">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            {pillars.map((pillar) => (
              <div
                key={pillar.key}
                className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-b from-white/5 to-transparent p-6 backdrop-blur-sm transition hover:border-white/20"
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${pillar.gradient} opacity-0 transition group-hover:opacity-10`} />
                <div className="relative">
                  <div className={`inline-flex rounded-xl bg-gradient-to-br ${pillar.gradient} p-2.5`}>
                    <pillar.icon className="h-5 w-5 text-white" />
                  </div>
                  <h3 className="mt-4 text-xl font-bold">{pillar.title}</h3>
                  <p className="mt-2 text-sm text-gray-400">{pillar.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Products */}
      <section id="products" className="py-12">
        <div className="mx-auto max-w-6xl px-6">
          <div className="mb-8">
            <h2 className="text-3xl font-bold md:text-4xl">Developer Tools</h2>
            <p className="mt-2 text-base text-gray-400">
              Production-ready primitives for every layer of your stack.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {products.map((product) => {
              const Icon = product.icon;
              return (
                <a
                  key={product.name}
                  href={product.href}
                  className="group relative overflow-hidden rounded-xl border border-white/10 bg-gradient-to-b from-white/5 to-transparent p-5 backdrop-blur-sm transition hover:border-white/20"
                >
                  <div className={`absolute inset-0 bg-gradient-to-br ${product.color} opacity-0 transition group-hover:opacity-10`} />
                  <div className="relative">
                    <div className={`inline-flex rounded-lg bg-gradient-to-br ${product.color} p-2`}>
                      <Icon className="h-4 w-4 text-white" />
                    </div>
                    <h3 className="mt-3 text-base font-bold">{product.name}</h3>
                    <p className="mt-1 text-xs text-gray-400">{product.tagline}</p>
                  </div>
                </a>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <h2 className="text-3xl font-bold md:text-4xl">
            Start building on Celara
          </h2>
          <p className="mt-4 text-base text-gray-400">
            Join hundreds of operators running production validators with Celara infrastructure.
          </p>
          <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
            <Button className="bg-gradient-to-r from-orbit to-plasma">
              Get Started Free
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button variant="outline" className="border-white/20 bg-transparent hover:bg-white/5">
              Talk to Sales
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-8">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            <div>
              <div className="text-sm font-semibold text-white">Product</div>
              <div className="mt-3 space-y-2">
                {["Infrastructure", "Security", "Platform", "Pricing"].map((item) => (
                  <div key={item}>
                    <a href="#" className="text-sm text-gray-500 hover:text-gray-300">{item}</a>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <div className="text-sm font-semibold text-white">Developers</div>
              <div className="mt-3 space-y-2">
                {["Documentation", "API Reference", "GitHub", "Discord"].map((item) => (
                  <div key={item}>
                    <a href="#" className="text-sm text-gray-500 hover:text-gray-300">{item}</a>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <div className="text-sm font-semibold text-white">Company</div>
              <div className="mt-3 space-y-2">
                {["About", "Blog", "Careers", "Contact"].map((item) => (
                  <div key={item}>
                    <a href="#" className="text-sm text-gray-500 hover:text-gray-300">{item}</a>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <div className="text-sm font-semibold text-white">Legal</div>
              <div className="mt-3 space-y-2">
                {["Privacy", "Terms", "Security"].map((item) => (
                  <div key={item}>
                    <a href="#" className="text-sm text-gray-500 hover:text-gray-300">{item}</a>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="mt-8 flex flex-col items-center justify-between gap-3 border-t border-white/5 pt-6 md:flex-row">
            <div className="flex items-center gap-2.5">
              <div className="h-6 w-6 rounded-lg bg-gradient-to-tr from-orbit to-nebula" />
              <span className="text-sm font-semibold">Celara</span>
            </div>
            <p className="text-xs text-gray-600">© {new Date().getFullYear()} Celara Technologies, LLC</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
