import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowRight, Shield, ServerCog, Database, Network, LineChart, KeyRound, Layers, Globe, GitBranch, Code2, Terminal, Boxes } from "lucide-react";

const products = [
  {
    name: "NodeQuick",
    tagline: "Infrastructure-as-Code for validators",
    description: "Provision and manage blockchain validators across any chain with Terraform-like simplicity.",
    color: "from-[#4C6FFF] to-[#6B3DF4]",
    icon: ServerCog,
    href: "/products/nodequick",
    pillar: "infrastructure",
  },
  {
    name: "ChainWatch",
    tagline: "Observability for decentralized systems",
    description: "Monitor validators, RPC nodes, and clusters with Prometheus + Grafana integration.",
    color: "from-[#6366F1] to-[#6B3DF4]",
    icon: LineChart,
    href: "/products/chainwatch",
    pillar: "infrastructure",
  },
  {
    name: "ChainETL",
    tagline: "Blockchain data pipelines",
    description: "Stream on-chain data to S3, BigQuery, or Snowflake for analytics and compliance.",
    color: "from-[#6B3DF4] to-[#9333EA]",
    icon: Database,
    href: "/products/chainetl",
    pillar: "infrastructure",
  },
  {
    name: "SecurityKit",
    tagline: "Automated security for smart contracts",
    description: "CI/CD security checks, key management, and audit automation for Rust and Solidity.",
    color: "from-[#F59E0B] to-[#FB7185]",
    icon: KeyRound,
    href: "/products/securitykit",
    pillar: "security",
  },
  {
    name: "DAOForm",
    tagline: "Governance-as-Code",
    description: "Define and deploy DAO configurations with YAML. Version control your governance.",
    color: "from-[#F05AFF] to-[#F59E0B]",
    icon: GitBranch,
    href: "/products/daoform",
    pillar: "security",
  },
  {
    name: "ValidatorHub",
    tagline: "Operator economics dashboard",
    description: "Track validator performance, rewards, and ROI across multiple chains in real-time.",
    color: "from-[#14B8A6] to-[#22D3EE]",
    icon: Layers,
    href: "/products/validatorhub",
    pillar: "security",
  },
  {
    name: "RunNode Cloud",
    tagline: "Managed control plane",
    description: "SaaS platform for operating validators with enterprise reliability and compliance.",
    color: "from-[#6B7280] to-[#9CA3AF]",
    icon: Globe,
    href: "/runnode",
    pillar: "platform",
  },
  {
    name: "Celara Network",
    tagline: "Federated validator mesh",
    description: "DePIN-style operator registry with on-chain discovery and reputation scoring.",
    color: "from-[#4C6FFF] to-[#2DD4BF]",
    icon: Network,
    href: "/network",
    pillar: "platform",
  },
];

const pillars = [
  {
    key: "infrastructure",
    title: "Infrastructure",
    subtitle: "Build & Deploy",
    description: "Provision, monitor, and scale blockchain infrastructure with cloud-grade automation.",
    icon: Boxes,
    gradient: "from-[#4C6FFF] to-[#6B3DF4]",
  },
  {
    key: "security",
    title: "Security",
    subtitle: "Harden & Govern",
    description: "Automated security checks, key management, and governance-as-code for decentralized systems.",
    icon: Shield,
    gradient: "from-[#FB923C] to-[#F05AFF]",
  },
  {
    key: "platform",
    title: "Platform",
    subtitle: "Operate & Scale",
    description: "Managed services and federated networks for enterprise-grade validator operations.",
    icon: Globe,
    gradient: "from-[#2DD4BF] to-[#4C6FFF]",
  },
];

export default function CelaraLanding() {
  return (
    <div className="min-h-screen w-full bg-black text-white">
      {/* Nav */}
      <header className="fixed top-0 z-50 w-full border-b border-white/5 bg-black/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-orbit to-nebula" />
            <span className="text-lg font-semibold tracking-tight">Celara</span>
          </div>
          <nav className="hidden items-center gap-8 md:flex">
            <a className="text-sm text-gray-400 transition hover:text-white" href="#ecosystem">Ecosystem</a>
            <a className="text-sm text-gray-400 transition hover:text-white" href="#products">Products</a>
            <a className="text-sm text-gray-400 transition hover:text-white" href="/docs">Docs</a>
            <a className="text-sm text-gray-400 transition hover:text-white" href="/open">Open Source</a>
          </nav>
          <div className="flex items-center gap-3">
            <Button variant="secondary" className="hidden md:inline-flex">GitHub</Button>
            <Button className="bg-gradient-to-r from-orbit to-plasma">Launch Cloud</Button>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden pt-32 pb-20">
        {/* Gradient orbs */}
        <div className="absolute top-0 left-1/4 h-96 w-96 rounded-full bg-orbit/20 blur-3xl" />
        <div className="absolute top-20 right-1/4 h-96 w-96 rounded-full bg-nebula/20 blur-3xl" />
        
        <div className="relative mx-auto max-w-7xl px-6 text-center">
          <Badge className="mb-6 border-white/10 bg-white/5 text-white backdrop-blur-sm">
            Infrastructure for Decentralized Systems
          </Badge>
          <h1 className="mx-auto max-w-4xl text-5xl font-bold leading-tight tracking-tight md:text-7xl">
            Build, secure, and operate{" "}
            <span className="bg-gradient-to-r from-orbit via-plasma to-nebula bg-clip-text text-transparent">
              blockchain infrastructure
            </span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-400 md:text-xl">
            Modular, open-source primitives that professionalize how decentralized systems are built, monitored, and secured. From validators to DAOs.
          </p>
          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Button size="lg" className="bg-gradient-to-r from-orbit to-plasma text-base">
              Explore Ecosystem
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline" className="border-white/20 bg-transparent text-base hover:bg-white/5">
              Read Documentation
            </Button>
          </div>

          {/* Stats */}
          <div className="mt-20 grid grid-cols-2 gap-8 md:grid-cols-4">
            {[
              { label: "Open Source Tools", value: "8" },
              { label: "Chains Supported", value: "12+" },
              { label: "GitHub Stars", value: "2.4K" },
              { label: "Active Validators", value: "500+" },
            ].map((stat) => (
              <div key={stat.label} className="rounded-2xl border border-white/5 bg-white/5 p-6 backdrop-blur-sm">
                <div className="text-3xl font-bold text-white md:text-4xl">{stat.value}</div>
                <div className="mt-2 text-sm text-gray-400">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Ecosystem Pillars */}
      <section id="ecosystem" className="py-20">
        <div className="mx-auto max-w-7xl px-6">
          <div className="mb-16 text-center">
            <h2 className="text-3xl font-bold md:text-5xl">The Celara Ecosystem</h2>
            <p className="mt-4 text-lg text-gray-400">
              Three pillars. One unified platform for decentralized infrastructure.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            {pillars.map((pillar) => (
              <div
                key={pillar.key}
                className="group relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-b from-white/5 to-transparent p-8 backdrop-blur-sm transition hover:border-white/20"
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${pillar.gradient} opacity-0 transition group-hover:opacity-10`} />
                <div className="relative">
                  <div className={`inline-flex rounded-2xl bg-gradient-to-br ${pillar.gradient} p-3`}>
                    <pillar.icon className="h-6 w-6 text-white" />
                  </div>
                  <div className="mt-6">
                    <div className="text-sm font-medium text-gray-400">{pillar.subtitle}</div>
                    <h3 className="mt-2 text-2xl font-bold">{pillar.title}</h3>
                    <p className="mt-4 text-gray-400">{pillar.description}</p>
                  </div>
                  <div className="mt-6 flex items-center gap-2 text-sm font-medium">
                    <span className={`bg-gradient-to-r ${pillar.gradient} bg-clip-text text-transparent`}>
                      Explore tools
                    </span>
                    <ArrowRight className="h-4 w-4 text-gray-400 transition group-hover:translate-x-1" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Products */}
      <section id="products" className="py-20">
        <div className="mx-auto max-w-7xl px-6">
          <div className="mb-16">
            <h2 className="text-3xl font-bold md:text-5xl">Developer Tools</h2>
            <p className="mt-4 text-lg text-gray-400">
              Production-ready primitives for every layer of your stack.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            {products.map((product) => {
              const Icon = product.icon;
              return (
                <a
                  key={product.name}
                  href={product.href}
                  className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-b from-white/5 to-transparent p-6 backdrop-blur-sm transition hover:border-white/20 hover:shadow-2xl"
                >
                  <div className={`absolute inset-0 bg-gradient-to-br ${product.color} opacity-0 transition group-hover:opacity-10`} />
                  <div className="relative">
                    <div className={`inline-flex rounded-xl bg-gradient-to-br ${product.color} p-2.5`}>
                      <Icon className="h-5 w-5 text-white" />
                    </div>
                    <h3 className="mt-4 text-xl font-bold">{product.name}</h3>
                    <p className="mt-1 text-sm font-medium text-gray-400">{product.tagline}</p>
                    <p className="mt-3 text-sm text-gray-500">{product.description}</p>
                    <div className="mt-4 flex items-center gap-2 text-sm font-medium">
                      <span className={`bg-gradient-to-r ${product.color} bg-clip-text text-transparent`}>
                        Learn more
                      </span>
                      <ArrowRight className="h-4 w-4 text-gray-400 transition group-hover:translate-x-1" />
                    </div>
                  </div>
                </a>
              );
            })}
          </div>
        </div>
      </section>

      {/* Developer Experience */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-6">
          <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-b from-white/5 to-transparent backdrop-blur-sm">
            <div className="grid grid-cols-1 gap-12 p-12 md:grid-cols-2 md:gap-16">
              <div>
                <div className="inline-flex rounded-2xl bg-gradient-to-br from-orbit to-plasma p-3">
                  <Code2 className="h-6 w-6 text-white" />
                </div>
                <h3 className="mt-6 text-3xl font-bold">Built for developers</h3>
                <p className="mt-4 text-gray-400">
                  Infrastructure-as-code, GitOps workflows, and CI/CD integrations. Deploy validators like you deploy applications.
                </p>
                <div className="mt-8 space-y-4">
                  {[
                    "Terraform & Pulumi providers",
                    "GitHub Actions & GitLab CI",
                    "Kubernetes operators",
                    "REST & GraphQL APIs",
                  ].map((feature) => (
                    <div key={feature} className="flex items-center gap-3">
                      <div className="h-1.5 w-1.5 rounded-full bg-gradient-to-r from-orbit to-plasma" />
                      <span className="text-sm text-gray-300">{feature}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-black/50 p-6 font-mono text-sm">
                <div className="flex items-center gap-2 border-b border-white/10 pb-3">
                  <Terminal className="h-4 w-4 text-gray-400" />
                  <span className="text-gray-400">quickstart.sh</span>
                </div>
                <div className="mt-4 space-y-2 text-gray-400">
                  <div><span className="text-plasma">$</span> npm install -g @celara/cli</div>
                  <div><span className="text-plasma">$</span> celara init solana-validator</div>
                  <div><span className="text-plasma">$</span> celara deploy --chain solana</div>
                  <div className="pt-2 text-teal">✓ Validator deployed in 47s</div>
                  <div className="text-gray-500">→ https://solana.fm/validator/...</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <h2 className="text-4xl font-bold md:text-5xl">
            Start building on Celara
          </h2>
          <p className="mt-6 text-lg text-gray-400">
            Join hundreds of operators running production validators with Celara infrastructure.
          </p>
          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Button size="lg" className="bg-gradient-to-r from-orbit to-plasma text-base">
              Get Started Free
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline" className="border-white/20 bg-transparent text-base hover:bg-white/5">
              Talk to Sales
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-12">
        <div className="mx-auto max-w-7xl px-6">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            <div>
              <div className="text-sm font-semibold">Product</div>
              <div className="mt-4 space-y-3">
                {["Infrastructure", "Security", "Platform", "Pricing"].map((item) => (
                  <div key={item}>
                    <a href="#" className="text-sm text-gray-400 hover:text-white">{item}</a>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <div className="text-sm font-semibold">Developers</div>
              <div className="mt-4 space-y-3">
                {["Documentation", "API Reference", "GitHub", "Discord"].map((item) => (
                  <div key={item}>
                    <a href="#" className="text-sm text-gray-400 hover:text-white">{item}</a>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <div className="text-sm font-semibold">Company</div>
              <div className="mt-4 space-y-3">
                {["About", "Blog", "Careers", "Contact"].map((item) => (
                  <div key={item}>
                    <a href="#" className="text-sm text-gray-400 hover:text-white">{item}</a>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <div className="text-sm font-semibold">Legal</div>
              <div className="mt-4 space-y-3">
                {["Privacy", "Terms", "Security", "Compliance"].map((item) => (
                  <div key={item}>
                    <a href="#" className="text-sm text-gray-400 hover:text-white">{item}</a>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-white/5 pt-8 md:flex-row">
            <div className="flex items-center gap-3">
              <div className="h-6 w-6 rounded-lg bg-gradient-to-tr from-orbit to-nebula" />
              <span className="text-sm font-semibold">Celara</span>
            </div>
            <p className="text-sm text-gray-500">© {new Date().getFullYear()} Celara Technologies, LLC. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
