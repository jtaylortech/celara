import { Button } from "@/components/ui/button";
import { ArrowRight, Github } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section className="relative overflow-hidden px-6 pt-40 pb-32">
        {/* Vibrant gradient background */}
        <div className="absolute inset-0 -z-10 bg-gradient-to-br from-[#0E0E11] via-[#1a1a2e] to-[#0E0E11]">
          <div className="absolute top-0 left-1/4 h-[800px] w-[800px] rounded-full bg-[#FFE66D] opacity-20 blur-[200px]" />
          <div className="absolute top-40 right-1/4 h-[800px] w-[800px] rounded-full bg-[#4C6FFF] opacity-20 blur-[200px]" />
          <div className="absolute bottom-0 left-1/2 h-[600px] w-[600px] rounded-full bg-[#F05AFF] opacity-15 blur-[180px]" />
        </div>
        
        <div className="relative mx-auto max-w-6xl text-center">
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-[#FFE66D]/20 bg-[#FFE66D]/5 px-5 py-2 backdrop-blur-sm">
            <span className="text-sm font-medium text-[#FFE66D]">Infrastructure for Decentralized Systems</span>
          </div>
          
          <h1 className="text-6xl font-bold leading-[1.1] tracking-tight md:text-8xl">
            The <span className="bg-gradient-to-r from-[#FFE66D] via-[#FDB927] to-[#FFE66D] bg-clip-text text-transparent">HashiCorp</span><br />
            of Web3
          </h1>
          
          <p className="mx-auto mt-8 max-w-2xl text-xl leading-relaxed text-[#A3A3AD]">
            Open-source primitives that bring DevOps discipline to blockchain infrastructure.
          </p>
          
          <div className="mt-12 flex flex-wrap items-center justify-center gap-4">
            <Button size="lg" className="h-14 bg-gradient-to-r from-[#FFE66D] to-[#FDB927] px-8 text-base font-semibold text-black shadow-lg shadow-[#FFE66D]/20 hover:shadow-xl hover:shadow-[#FFE66D]/30">
              Get Started
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline" className="h-14 border-white/20 bg-white/5 px-8 text-base backdrop-blur-sm hover:bg-white/10">
              <Github className="mr-2 h-5 w-5" />
              GitHub
            </Button>
          </div>
        </div>
      </section>

      {/* Products - Horizontal Showcase */}
      <section className="px-6 py-32">
        <div className="mx-auto max-w-7xl">
          <div className="mb-20 text-center">
            <h2 className="text-5xl font-bold md:text-6xl">The Stack</h2>
            <p className="mt-4 text-xl text-[#A3A3AD]">Deploy. Watch. Secure. Govern.</p>
          </div>
          
          <div className="space-y-6">
            {/* ChainOps */}
            <Link href="/products/chainops" className="group block">
              <div className="relative overflow-hidden rounded-3xl border border-[#FFE66D]/20 bg-gradient-to-br from-[#FFE66D]/10 via-transparent to-transparent p-12 transition hover:border-[#FFE66D]/40 hover:shadow-2xl hover:shadow-[#FFE66D]/10">
                <div className="flex flex-col items-start gap-8 md:flex-row md:items-center md:justify-between">
                  <div className="flex-1">
                    <div className="mb-4 inline-flex items-center gap-3 rounded-full bg-[#FFE66D]/10 px-4 py-2">
                      <div className="h-2 w-2 rounded-full bg-[#FFE66D]" />
                      <span className="text-sm font-semibold text-[#FFE66D]">INFRASTRUCTURE</span>
                    </div>
                    <h3 className="text-4xl font-bold">ChainOps</h3>
                    <p className="mt-4 text-lg text-[#A3A3AD]">Deploy validators like cloud infrastructure. Terraform for blockchain.</p>
                  </div>
                  <div className="flex items-center gap-3 text-white">
                    <span className="text-sm font-medium">Explore</span>
                    <ArrowRight className="h-5 w-5 transition group-hover:translate-x-2" />
                  </div>
                </div>
              </div>
            </Link>

            {/* ChainWatch */}
            <Link href="/products/chainwatch" className="group block">
              <div className="relative overflow-hidden rounded-3xl border border-[#4C6FFF]/20 bg-gradient-to-br from-[#4C6FFF]/10 via-transparent to-transparent p-12 transition hover:border-[#4C6FFF]/40 hover:shadow-2xl hover:shadow-[#4C6FFF]/10">
                <div className="flex flex-col items-start gap-8 md:flex-row md:items-center md:justify-between">
                  <div className="flex-1">
                    <div className="mb-4 inline-flex items-center gap-3 rounded-full bg-[#4C6FFF]/10 px-4 py-2">
                      <div className="h-2 w-2 rounded-full bg-[#4C6FFF]" />
                      <span className="text-sm font-semibold text-[#4C6FFF]">OBSERVABILITY</span>
                    </div>
                    <h3 className="text-4xl font-bold">ChainWatch</h3>
                    <p className="mt-4 text-lg text-[#A3A3AD]">Real-time monitoring for decentralized systems. Datadog for blockchain.</p>
                  </div>
                  <div className="flex items-center gap-3 text-white">
                    <span className="text-sm font-medium">Explore</span>
                    <ArrowRight className="h-5 w-5 transition group-hover:translate-x-2" />
                  </div>
                </div>
              </div>
            </Link>

            {/* SecurityKit */}
            <Link href="/products/securitykit" className="group block">
              <div className="relative overflow-hidden rounded-3xl border border-[#F05AFF]/20 bg-gradient-to-br from-[#F05AFF]/10 via-transparent to-transparent p-12 transition hover:border-[#F05AFF]/40 hover:shadow-2xl hover:shadow-[#F05AFF]/10">
                <div className="flex flex-col items-start gap-8 md:flex-row md:items-center md:justify-between">
                  <div className="flex-1">
                    <div className="mb-4 inline-flex items-center gap-3 rounded-full bg-[#F05AFF]/10 px-4 py-2">
                      <div className="h-2 w-2 rounded-full bg-[#F05AFF]" />
                      <span className="text-sm font-semibold text-[#F05AFF]">SECURITY</span>
                    </div>
                    <h3 className="text-4xl font-bold">SecurityKit</h3>
                    <p className="mt-4 text-lg text-[#A3A3AD]">Automated security for node operators. Vault for blockchain.</p>
                  </div>
                  <div className="flex items-center gap-3 text-white">
                    <span className="text-sm font-medium">Explore</span>
                    <ArrowRight className="h-5 w-5 transition group-hover:translate-x-2" />
                  </div>
                </div>
              </div>
            </Link>

            {/* ChainETL + DAOForm - Side by side */}
            <div className="grid gap-6 md:grid-cols-2">
              <Link href="/products/chainetl" className="group block">
                <div className="relative h-full overflow-hidden rounded-3xl border border-[#6B3DF4]/20 bg-gradient-to-br from-[#6B3DF4]/10 via-transparent to-transparent p-10 transition hover:border-[#6B3DF4]/40 hover:shadow-2xl hover:shadow-[#6B3DF4]/10">
                  <div className="mb-4 inline-flex items-center gap-3 rounded-full bg-[#6B3DF4]/10 px-4 py-2">
                    <div className="h-2 w-2 rounded-full bg-[#6B3DF4]" />
                    <span className="text-sm font-semibold text-[#6B3DF4]">DATA</span>
                  </div>
                  <h3 className="text-3xl font-bold">ChainETL</h3>
                  <p className="mt-4 text-[#A3A3AD]">Blockchain data pipelines</p>
                  <div className="mt-6 flex items-center gap-2 text-white">
                    <span className="text-sm font-medium">Explore</span>
                    <ArrowRight className="h-4 w-4 transition group-hover:translate-x-2" />
                  </div>
                </div>
              </Link>

              <Link href="/products/daoform" className="group block">
                <div className="relative h-full overflow-hidden rounded-3xl border border-[#2DD4BF]/20 bg-gradient-to-br from-[#2DD4BF]/10 via-transparent to-transparent p-10 transition hover:border-[#2DD4BF]/40 hover:shadow-2xl hover:shadow-[#2DD4BF]/10">
                  <div className="mb-4 inline-flex items-center gap-3 rounded-full bg-[#2DD4BF]/10 px-4 py-2">
                    <div className="h-2 w-2 rounded-full bg-[#2DD4BF]" />
                    <span className="text-sm font-semibold text-[#2DD4BF]">GOVERNANCE</span>
                  </div>
                  <h3 className="text-3xl font-bold">DAOForm</h3>
                  <p className="mt-4 text-[#A3A3AD]">Governance-as-Code</p>
                  <div className="mt-6 flex items-center gap-2 text-white">
                    <span className="text-sm font-medium">Explore</span>
                    <ArrowRight className="h-4 w-4 transition group-hover:translate-x-2" />
                  </div>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Statement */}
      <section className="px-6 py-32">
        <div className="mx-auto max-w-5xl text-center">
          <h2 className="text-5xl font-bold leading-tight md:text-7xl">
            Where others chase speculation,<br />
            we build <span className="bg-gradient-to-r from-[#FFE66D] to-[#FDB927] bg-clip-text text-transparent">permanence</span>
          </h2>
        </div>
      </section>

      {/* Open Source */}
      <section className="px-6 py-32">
        <div className="mx-auto max-w-7xl">
          <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-[#FFE66D]/5 via-[#4C6FFF]/5 to-[#F05AFF]/5 p-20 text-center backdrop-blur-sm">
            <h2 className="text-5xl font-bold md:text-6xl">Open Source First</h2>
            <p className="mx-auto mt-6 max-w-2xl text-xl text-[#A3A3AD]">
              MIT-licensed core. Public metrics. Community-driven.
            </p>
            <div className="mt-12 flex flex-wrap items-center justify-center gap-4">
              <Button size="lg" variant="outline" className="h-14 border-white/20 bg-white/5 px-8 text-base backdrop-blur-sm hover:bg-white/10">
                <Github className="mr-2 h-5 w-5" />
                View Repositories
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="px-6 py-32">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="text-5xl font-bold md:text-6xl">Start building</h2>
          <p className="mt-6 text-xl text-[#A3A3AD]">
            Join operators running production validators with Celara.
          </p>
          <div className="mt-12">
            <Button size="lg" className="h-16 bg-gradient-to-r from-[#FFE66D] to-[#FDB927] px-12 text-lg font-semibold text-black shadow-2xl shadow-[#FFE66D]/20 hover:shadow-[#FFE66D]/30">
              Get Started Free
              <ArrowRight className="ml-2 h-6 w-6" />
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
