import { Button } from "@/components/ui/button";
import { ProductCard } from "@/components/ui/product-card";
import { ArrowRight, Github, ServerCog, LineChart, Shield, Database, GitBranch } from "lucide-react";

const products = [
  {
    title: "ChainOps",
    description: "Infrastructure-as-Code for validators. Deploy blockchain infrastructure like cloud-native systems.",
    href: "/products/chainops",
    icon: ServerCog,
    gradient: "from-[#FFE66D] to-[#FDB927]",
  },
  {
    title: "ChainWatch",
    description: "Observability for decentralized systems. Know your uptime, track your health, prove your reliability.",
    href: "/products/chainwatch",
    icon: LineChart,
    gradient: "from-[#4C6FFF] to-[#6B3DF4]",
  },
  {
    title: "SecurityKit",
    description: "Security and compliance for node operators. From KMS integrations to threat detection.",
    href: "/products/securitykit",
    icon: Shield,
    gradient: "from-[#F05AFF] to-[#FDB927]",
  },
  {
    title: "ChainETL",
    description: "Blockchain data pipelines. Extract, transform, and load on-chain data into standardized schemas.",
    href: "/products/chainetl",
    icon: Database,
    gradient: "from-[#6B3DF4] to-[#F05AFF]",
  },
  {
    title: "DAOForm",
    description: "Governance-as-Code. Off-chain coordination with on-chain execution for DAOs.",
    href: "/products/daoform",
    icon: GitBranch,
    gradient: "from-[#2DD4BF] to-[#4C6FFF]",
  },
];

const pillars = [
  {
    title: "Clarity → Code as Infrastructure",
    description: "Decentralization shouldn't mean disorder. Celara brings reproducibility, security, and visibility to blockchain operations.",
  },
  {
    title: "Transparency → Open Core, Not Black Box",
    description: "Trust is earned through visibility. Celara's core is open, auditable, and community-driven.",
  },
  {
    title: "Security → Trust Through Design",
    description: "Every Celara primitive is built around operational safety — isolation, encryption, observability, compliance.",
  },
];

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section className="relative overflow-hidden px-6 pt-32 pb-20">
        <div className="absolute top-0 left-1/4 h-[500px] w-[500px] rounded-full bg-[#FFE66D]/10 blur-[120px]" />
        <div className="absolute top-20 right-1/4 h-[500px] w-[500px] rounded-full bg-[#FDB927]/10 blur-[120px]" />
        
        <div className="relative mx-auto max-w-5xl text-center">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm backdrop-blur-sm">
            <span className="text-[#A3A3AD]">Infrastructure for Decentralized Systems</span>
          </div>
          
          <h1 className="text-5xl font-bold leading-tight tracking-tight md:text-7xl">
            Professionalize how<br />
            <span className="bg-gradient-to-r from-[#FFE66D] to-[#FDB927] bg-clip-text text-transparent">
              decentralized systems
            </span>
            <br />are built
          </h1>
          
          <p className="mx-auto mt-6 max-w-2xl text-lg text-[#A3A3AD]">
            Modular, open-source primitives for validators, RPCs, and DAOs. From deployment to monitoring to governance automation.
          </p>
          
          <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
            <Button size="lg" className="bg-gradient-to-r from-[#FFE66D] to-[#FDB927] text-black hover:opacity-90">
              Get Started
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button size="lg" variant="outline" className="border-white/20 bg-transparent hover:bg-white/5">
              <Github className="mr-2 h-4 w-4" />
              View on GitHub
            </Button>
          </div>
        </div>
      </section>

      {/* Products */}
      <section className="px-6 py-20">
        <div className="mx-auto max-w-7xl">
          <div className="mb-12">
            <h2 className="text-3xl font-bold md:text-4xl">The Celara Stack</h2>
            <p className="mt-3 text-lg text-[#A3A3AD]">
              Deploy. Watch. Secure. Govern. Repeat.
            </p>
          </div>
          
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {products.map((product) => (
              <ProductCard key={product.title} {...product} />
            ))}
          </div>
        </div>
      </section>

      {/* Why Celara */}
      <section className="px-6 py-20">
        <div className="mx-auto max-w-7xl">
          <div className="mb-12 text-center">
            <h2 className="text-3xl font-bold md:text-4xl">Why Celara</h2>
            <p className="mt-3 text-lg text-[#A3A3AD]">
              Open tools. Reliable systems. Professional-grade decentralization.
            </p>
          </div>
          
          <div className="grid gap-8 md:grid-cols-3">
            {pillars.map((pillar, i) => (
              <div key={i} className="rounded-xl border border-white/10 bg-[#16161A] p-8">
                <h3 className="text-xl font-semibold">{pillar.title}</h3>
                <p className="mt-4 text-[#A3A3AD]">{pillar.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Architecture */}
      <section className="px-6 py-20">
        <div className="mx-auto max-w-5xl">
          <div className="rounded-2xl border border-white/10 bg-[#16161A] p-12 text-center">
            <h2 className="text-2xl font-bold md:text-3xl">
              Cloud had HashiCorp.<br />
              Decentralized systems have Celara.
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-[#A3A3AD]">
              Where others chase speculation, Celara builds permanence: secure, modular, open infrastructure for a world that runs on code, not custodians.
            </p>
          </div>
        </div>
      </section>

      {/* Open Source */}
      <section className="px-6 py-20">
        <div className="mx-auto max-w-7xl">
          <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-[#FFE66D]/5 to-[#FDB927]/5 p-12 text-center">
            <h2 className="text-3xl font-bold md:text-4xl">Open Source First</h2>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-[#A3A3AD]">
              We don't hide reliability behind NDAs — we publish it. MIT-licensed core modules, public metrics, community-driven validation.
            </p>
            <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
              <Button size="lg" variant="outline" className="border-white/20 bg-transparent hover:bg-white/5">
                <Github className="mr-2 h-4 w-4" />
                Explore Repositories
              </Button>
              <Button size="lg" variant="outline" className="border-white/20 bg-transparent hover:bg-white/5">
                Contribute
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="px-6 py-20">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="text-3xl font-bold md:text-4xl">
            Start building on Celara
          </h2>
          <p className="mt-4 text-lg text-[#A3A3AD]">
            Join operators running production validators with Celara infrastructure.
          </p>
          <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
            <Button size="lg" className="bg-gradient-to-r from-[#FFE66D] to-[#FDB927] text-black hover:opacity-90">
              Get Started Free
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button size="lg" variant="outline" className="border-white/20 bg-transparent hover:bg-white/5">
              View Documentation
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
