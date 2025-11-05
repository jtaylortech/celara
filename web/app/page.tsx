import { Button } from "@/components/ui/button";
import { ArrowRight, Github, Terminal, Eye, Lock, Database, Vote } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section className="relative overflow-hidden px-6 py-30">
        {/* Gradient background */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 left-1/4 h-[600px] w-[600px] rounded-full bg-accent-1/20 blur-[150px]" />
          <div className="absolute top-40 right-1/4 h-[600px] w-[600px] rounded-full bg-accent-2/20 blur-[150px]" />
        </div>
        
        <div className="container-celara">
          <div className="mx-auto max-w-4xl text-center">
            <h1 className="text-h1 md:text-[80px]">
              Infrastructure for<br />
              Decentralized Systems
            </h1>
            
            <p className="mx-auto mt-8 max-w-2xl text-body text-muted">
              Open-source primitives that bring DevOps discipline to blockchain infrastructure.
            </p>
            
            <div className="mt-12 flex flex-wrap items-center justify-center gap-4">
              <Button size="lg">
                Get Started
                <ArrowRight className="h-5 w-5" />
              </Button>
              <Button size="lg" variant="secondary">
                <Github className="h-5 w-5" />
                GitHub
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Products */}
      <section className="px-6 py-30">
        <div className="container-celara">
          <div className="mb-16 text-center">
            <h2 className="text-h2">The Stack</h2>
            <p className="mt-4 text-body text-muted">Deploy. Watch. Secure. Govern.</p>
          </div>
          
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {/* ChainOps */}
            <Link href="/products/chainops" className="group block">
              <div className="relative overflow-hidden rounded-lg border border-border bg-surface p-8 shadow-md transition-all hover:border-accent-1/50 hover:ring-solar">
                <div className="absolute inset-0 bg-gradient-to-br from-accent-1/0 to-accent-2/0 transition group-hover:from-accent-1/5 group-hover:to-accent-2/5" />
                <div className="relative">
                  <div className="inline-flex rounded-lg bg-solar-gradient p-3">
                    <Terminal className="h-6 w-6 text-bg" />
                  </div>
                  <h3 className="mt-6 text-h3">ChainOps</h3>
                  <p className="mt-3 text-muted">Deploy validators like cloud infrastructure</p>
                  <div className="mt-6 inline-flex items-center gap-2 text-sm font-medium">
                    Learn more
                    <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
                  </div>
                </div>
              </div>
            </Link>

            {/* ChainWatch */}
            <Link href="/products/chainwatch" className="group block">
              <div className="relative overflow-hidden rounded-lg border border-border bg-surface p-8 shadow-md transition-all hover:border-accent-1/50 hover:ring-solar">
                <div className="absolute inset-0 bg-gradient-to-br from-accent-1/0 to-accent-2/0 transition group-hover:from-accent-1/5 group-hover:to-accent-2/5" />
                <div className="relative">
                  <div className="inline-flex rounded-lg bg-solar-gradient p-3">
                    <Eye className="h-6 w-6 text-bg" />
                  </div>
                  <h3 className="mt-6 text-h3">ChainWatch</h3>
                  <p className="mt-3 text-muted">Observability for decentralized systems</p>
                  <div className="mt-6 inline-flex items-center gap-2 text-sm font-medium">
                    Learn more
                    <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
                  </div>
                </div>
              </div>
            </Link>

            {/* SecurityKit */}
            <Link href="/products/securitykit" className="group block">
              <div className="relative overflow-hidden rounded-lg border border-border bg-surface p-8 shadow-md transition-all hover:border-accent-1/50 hover:ring-solar">
                <div className="absolute inset-0 bg-gradient-to-br from-accent-1/0 to-accent-2/0 transition group-hover:from-accent-1/5 group-hover:to-accent-2/5" />
                <div className="relative">
                  <div className="inline-flex rounded-lg bg-solar-gradient p-3">
                    <Lock className="h-6 w-6 text-bg" />
                  </div>
                  <h3 className="mt-6 text-h3">SecurityKit</h3>
                  <p className="mt-3 text-muted">Automated security for node operators</p>
                  <div className="mt-6 inline-flex items-center gap-2 text-sm font-medium">
                    Learn more
                    <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
                  </div>
                </div>
              </div>
            </Link>

            {/* ChainETL */}
            <Link href="/products/chainetl" className="group block">
              <div className="relative overflow-hidden rounded-lg border border-border bg-surface p-8 shadow-md transition-all hover:border-accent-1/50 hover:ring-solar">
                <div className="absolute inset-0 bg-gradient-to-br from-accent-1/0 to-accent-2/0 transition group-hover:from-accent-1/5 group-hover:to-accent-2/5" />
                <div className="relative">
                  <div className="inline-flex rounded-lg bg-solar-gradient p-3">
                    <Database className="h-6 w-6 text-bg" />
                  </div>
                  <h3 className="mt-6 text-h3">ChainETL</h3>
                  <p className="mt-3 text-muted">Blockchain data pipelines</p>
                  <div className="mt-6 inline-flex items-center gap-2 text-sm font-medium">
                    Learn more
                    <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
                  </div>
                </div>
              </div>
            </Link>

            {/* DAOForm */}
            <Link href="/products/daoform" className="group block">
              <div className="relative overflow-hidden rounded-lg border border-border bg-surface p-8 shadow-md transition-all hover:border-accent-1/50 hover:ring-solar">
                <div className="absolute inset-0 bg-gradient-to-br from-accent-1/0 to-accent-2/0 transition group-hover:from-accent-1/5 group-hover:to-accent-2/5" />
                <div className="relative">
                  <div className="inline-flex rounded-lg bg-solar-gradient p-3">
                    <Vote className="h-6 w-6 text-bg" />
                  </div>
                  <h3 className="mt-6 text-h3">DAOForm</h3>
                  <p className="mt-3 text-muted">Governance-as-Code</p>
                  <div className="mt-6 inline-flex items-center gap-2 text-sm font-medium">
                    Learn more
                    <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
                  </div>
                </div>
              </div>
            </Link>
          </div>
        </div>
      </section>

      {/* Statement */}
      <section className="px-6 py-30">
        <div className="container-celara">
          <div className="mx-auto max-w-4xl text-center">
            <h2 className="text-h2 md:text-[56px] leading-tight">
              Cloud had HashiCorp.<br />
              Decentralized systems have <span className="bg-solar-gradient bg-clip-text text-transparent">Celara</span>.
            </h2>
          </div>
        </div>
      </section>

      {/* Open Source */}
      <section className="px-6 py-30">
        <div className="container-celara">
          <div className="relative overflow-hidden rounded-lg border border-border bg-gradient-to-br from-accent-1/10 via-transparent to-accent-2/10 p-20 text-center">
            <h2 className="text-h2">Open Source First</h2>
            <p className="mx-auto mt-6 max-w-2xl text-body text-muted">
              MIT-licensed core. Public metrics. Community-driven validation.
            </p>
            <div className="mt-12 flex flex-wrap items-center justify-center gap-4">
              <Button size="lg" variant="secondary">
                <Github className="h-5 w-5" />
                View Repositories
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="px-6 py-30">
        <div className="container-celara">
          <div className="mx-auto max-w-4xl text-center">
            <h2 className="text-h2">Start building</h2>
            <p className="mt-6 text-body text-muted">
              Join operators running production validators with Celara.
            </p>
            <div className="mt-12">
              <Button size="lg">
                Get Started Free
                <ArrowRight className="h-6 w-6" />
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
