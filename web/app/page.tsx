import { Button } from "@/components/ui/button";
import { ArrowRight, Github, Terminal, Eye, Lock, Database, Vote } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section className="relative overflow-hidden px-6 pt-40 pb-32">
        {/* Gradient mesh background */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 left-1/4 h-[600px] w-[600px] rounded-full bg-[#FFE66D]/20 blur-[150px] animate-pulse" />
          <div className="absolute top-40 right-1/4 h-[600px] w-[600px] rounded-full bg-[#FDB927]/20 blur-[150px] animate-pulse" style={{ animationDelay: '1s' }} />
        </div>
        
        <div className="relative mx-auto max-w-6xl">
          <div className="text-center">
            <h1 className="text-6xl font-bold leading-[1.1] tracking-tight md:text-8xl">
              Infrastructure for<br />
              <span className="bg-gradient-to-r from-[#FFE66D] via-[#FDB927] to-[#FFE66D] bg-clip-text text-transparent">
                Decentralized Systems
              </span>
            </h1>
            
            <p className="mx-auto mt-8 max-w-2xl text-xl text-[#A3A3AD]">
              Open-source primitives that bring DevOps discipline to blockchain infrastructure.
            </p>
            
            <div className="mt-12 flex flex-wrap items-center justify-center gap-4">
              <Button size="lg" className="h-14 bg-gradient-to-r from-[#FFE66D] to-[#FDB927] px-8 text-base font-semibold text-black hover:opacity-90">
                Get Started
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button size="lg" variant="outline" className="h-14 border-white/20 bg-transparent px-8 text-base hover:bg-white/5">
                <Github className="mr-2 h-5 w-5" />
                GitHub
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Products Grid */}
      <section className="px-6 py-32">
        <div className="mx-auto max-w-7xl">
          <div className="mb-16 text-center">
            <h2 className="text-4xl font-bold md:text-5xl">The Stack</h2>
            <p className="mt-4 text-xl text-[#A3A3AD]">Five tools. One mission.</p>
          </div>
          
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {/* ChainOps */}
            <Link href="/products/chainops" className="group relative overflow-hidden rounded-2xl border border-white/10 bg-[#16161A] p-8 transition hover:border-[#FFE66D]/50">
              <div className="absolute inset-0 bg-gradient-to-br from-[#FFE66D]/0 to-[#FDB927]/0 transition group-hover:from-[#FFE66D]/5 group-hover:to-[#FDB927]/5" />
              <div className="relative">
                <div className="inline-flex rounded-xl bg-gradient-to-br from-[#FFE66D] to-[#FDB927] p-3">
                  <Terminal className="h-6 w-6 text-black" />
                </div>
                <h3 className="mt-6 text-2xl font-bold">ChainOps</h3>
                <p className="mt-3 text-[#A3A3AD]">Deploy validators like cloud infrastructure</p>
                <div className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-white">
                  Learn more
                  <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
                </div>
              </div>
            </Link>

            {/* ChainWatch */}
            <Link href="/products/chainwatch" className="group relative overflow-hidden rounded-2xl border border-white/10 bg-[#16161A] p-8 transition hover:border-[#4C6FFF]/50">
              <div className="absolute inset-0 bg-gradient-to-br from-[#4C6FFF]/0 to-[#6B3DF4]/0 transition group-hover:from-[#4C6FFF]/5 group-hover:to-[#6B3DF4]/5" />
              <div className="relative">
                <div className="inline-flex rounded-xl bg-gradient-to-br from-[#4C6FFF] to-[#6B3DF4] p-3">
                  <Eye className="h-6 w-6 text-white" />
                </div>
                <h3 className="mt-6 text-2xl font-bold">ChainWatch</h3>
                <p className="mt-3 text-[#A3A3AD]">Observability for decentralized systems</p>
                <div className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-white">
                  Learn more
                  <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
                </div>
              </div>
            </Link>

            {/* SecurityKit */}
            <Link href="/products/securitykit" className="group relative overflow-hidden rounded-2xl border border-white/10 bg-[#16161A] p-8 transition hover:border-[#F05AFF]/50">
              <div className="absolute inset-0 bg-gradient-to-br from-[#F05AFF]/0 to-[#FDB927]/0 transition group-hover:from-[#F05AFF]/5 group-hover:to-[#FDB927]/5" />
              <div className="relative">
                <div className="inline-flex rounded-xl bg-gradient-to-br from-[#F05AFF] to-[#FDB927] p-3">
                  <Lock className="h-6 w-6 text-white" />
                </div>
                <h3 className="mt-6 text-2xl font-bold">SecurityKit</h3>
                <p className="mt-3 text-[#A3A3AD]">Automated security for node operators</p>
                <div className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-white">
                  Learn more
                  <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
                </div>
              </div>
            </Link>

            {/* ChainETL */}
            <Link href="/products/chainetl" className="group relative overflow-hidden rounded-2xl border border-white/10 bg-[#16161A] p-8 transition hover:border-[#6B3DF4]/50">
              <div className="absolute inset-0 bg-gradient-to-br from-[#6B3DF4]/0 to-[#F05AFF]/0 transition group-hover:from-[#6B3DF4]/5 group-hover:to-[#F05AFF]/5" />
              <div className="relative">
                <div className="inline-flex rounded-xl bg-gradient-to-br from-[#6B3DF4] to-[#F05AFF] p-3">
                  <Database className="h-6 w-6 text-white" />
                </div>
                <h3 className="mt-6 text-2xl font-bold">ChainETL</h3>
                <p className="mt-3 text-[#A3A3AD]">Blockchain data pipelines</p>
                <div className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-white">
                  Learn more
                  <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
                </div>
              </div>
            </Link>

            {/* DAOForm */}
            <Link href="/products/daoform" className="group relative overflow-hidden rounded-2xl border border-white/10 bg-[#16161A] p-8 transition hover:border-[#2DD4BF]/50">
              <div className="absolute inset-0 bg-gradient-to-br from-[#2DD4BF]/0 to-[#4C6FFF]/0 transition group-hover:from-[#2DD4BF]/5 group-hover:to-[#4C6FFF]/5" />
              <div className="relative">
                <div className="inline-flex rounded-xl bg-gradient-to-br from-[#2DD4BF] to-[#4C6FFF] p-3">
                  <Vote className="h-6 w-6 text-white" />
                </div>
                <h3 className="mt-6 text-2xl font-bold">DAOForm</h3>
                <p className="mt-3 text-[#A3A3AD]">Governance-as-Code</p>
                <div className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-white">
                  Learn more
                  <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
                </div>
              </div>
            </Link>
          </div>
        </div>
      </section>

      {/* Statement */}
      <section className="px-6 py-32">
        <div className="mx-auto max-w-5xl text-center">
          <h2 className="text-4xl font-bold leading-tight md:text-6xl">
            Cloud had HashiCorp.<br />
            Decentralized systems<br />
            have <span className="bg-gradient-to-r from-[#FFE66D] to-[#FDB927] bg-clip-text text-transparent">Celara</span>.
          </h2>
        </div>
      </section>

      {/* Open Source */}
      <section className="px-6 py-32">
        <div className="mx-auto max-w-7xl">
          <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-[#FFE66D]/10 via-transparent to-[#FDB927]/10 p-16 text-center">
            <div className="relative">
              <h2 className="text-4xl font-bold md:text-5xl">Open Source First</h2>
              <p className="mx-auto mt-6 max-w-2xl text-xl text-[#A3A3AD]">
                MIT-licensed core. Public metrics. Community-driven validation.
              </p>
              <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
                <Button size="lg" variant="outline" className="h-14 border-white/20 bg-transparent px-8 text-base hover:bg-white/5">
                  <Github className="mr-2 h-5 w-5" />
                  Explore Repositories
                </Button>
                <Button size="lg" variant="outline" className="h-14 border-white/20 bg-transparent px-8 text-base hover:bg-white/5">
                  Contribute
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="px-6 py-32">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="text-4xl font-bold md:text-5xl">
            Start building
          </h2>
          <p className="mt-6 text-xl text-[#A3A3AD]">
            Join operators running production validators with Celara.
          </p>
          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Button size="lg" className="h-14 bg-gradient-to-r from-[#FFE66D] to-[#FDB927] px-8 text-base font-semibold text-black hover:opacity-90">
              Get Started Free
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline" className="h-14 border-white/20 bg-transparent px-8 text-base hover:bg-white/5">
              Documentation
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
