We're gonna begin w dev work now! I dont know what is best, b/t react, next.js astro etc so we'll need to see. I really love https://www.hashicorp.com/en and esp the section in the screenshot w the infra, its descr, and related tools below it and same w security. You know what we're building and where it'd fall so let's def aim for that! We're shifting from naming it Jupiter tho to Celara ☀️ Celara Infrastructure for Decentralized Systems Modular, open-source primitives that professionalize how decentralized systems are built, monitored, and secured. Celara is to blockchain infrastructure what HashiCorp is to cloud computing. 🧭 Brand Architecture Celara Technologies, LLC │ ├── ChainOps Suite (Open Source) │ • NodeQuick – validator IaC & automation │ • ChainWatch – observability & metrics │ • ChainETL – blockchain data pipelines │ • DAOForm – governance-as-code │ • SecurityKit – program security & auditing │ • ValidatorHub – operator economics & analytics │ ├── RunNode Cloud (Commercial Platform) │ • Hosted control plane for multi-chain validators │ • Dashboards, alerting, scaling, HA, backups │ └── Celara Network (Federated Layer) • DePIN-style operator registry • On-chain validator discovery + peer reputation 💠 Brand & Site Structure (HashiCorp-Style) Section URL Purpose Home celara.dev Brand overview & value prop (“Infra for decentralized systems”) Docs Hub developer.celara.dev All product documentation (Terraform-style) Products Overview celara.dev/products Modular primitives grid (see below) Cloud Platform celara.dev/runnode SaaS dashboard, pricing, login Community / OSS celara.dev/open GitHub links, Discord, grants Network celara.dev/network Federation info & roadmap ⚙️ Product Family (HashiCorp adjacent mapping for design & positioning) Celara Product Function HashiCorp Analog Purpose / Tagline NodeQuick Infrastructure-as-Code for blockchain validators and RPCs Terraform Provision decentralized infrastructure anywhere. ChainWatch Metrics & observability stack (Prometheus + Grafana Helm) Consul / Datadog hybrid Monitor validators, RPC nodes, and clusters with precision. ChainETL Stream blockchain data → S3 / Athena / BigQuery Packer + Waypoint hybrid Pipeline data from on-chain to analytics lakes. DAOForm Governance-as-Code (YAML → DAO deployer) Terraform for governance Manage governance infra like you manage code. SecurityKit Smart contract security toolkit (Rust + Solidity) Vault / Boundary Automated security checks, keys, and audits for programs. ValidatorHub Economics & analytics dashboards Nomad (observability side) Understand costs, rewards, and validator ROI across chains. RunNode Cloud Hosted SaaS control plane for all above Terraform Cloud Operate validators and RPCs with managed reliability. Celara Network Federated DePIN validator mesh Consul Service Mesh Connect decentralized nodes via registry + reputation. 🪐 Brand System Element Spec Name Celara Meaning Derived from “celestial” + “ara” (Latin for altar) → the altar of the stars — evokes precision, scale, and calm authority Color Palette Orbit Blue #4C6FFF · Plasma Violet #6B3DF4 · Deep Space #0A0E29 · Nebula Pink #F05AFF · White #FFFFFF Typography Space Grotesk (headings) + Inter (body) Tone Scientific · Calm · Technical Design Language Gradient spectral ribbons (like Terraform/Vault), black canvas UI, neon accent highlights Favicon/Logo Minimal planetary arc (semi-circle ring) forming the letter “C” 🔧 Implementation Notes for Web / Dev Team Site Visual Layout (inspired by your screenshot) Top Hero Section: Dark cosmic gradient background Headline: “Infrastructure for Decentralized Systems” Subheadline: “Automate, observe, and secure blockchain operations — with cloud-grade reliability.” Two colored panels: Infrastructure Lifecycle → NodeQuick, ChainWatch, ChainETL Security Lifecycle → SecurityKit, DAOForm, ValidatorHub Below that: Grid of Celara tools with icons, each linking to /product-name. Color-code categories like HashiCorp (blue = infra, orange = security). Product Grid Example Product Shortline Color NodeQuick Provision & manage validators Blue ChainWatch Monitor and alert across nodes Indigo ChainETL Stream chain data to your cloud Violet SecurityKit Secure programs and keys Orange DAOForm Define and deploy DAO configs Pink ValidatorHub Track validator performance Teal RunNode Cloud SaaS orchestration plane Gray Celara Network Federated DePIN mesh Neutral Developer Docs Hierarchy developer.celara.dev/ │ ├── intro/ # overview, architecture diagrams ├── nodequick/ │ ├── install/ │ ├── providers/ │ ├── examples/ │ └── modules/ ├── chainwatch/ │ ├── setup/ │ ├── metrics/ │ └── dashboards/ ├── securitykit/ │ ├── audits/ │ ├── cli/ │ └── ci-cd/ └── daoform/ ├── syntax/ └── templates/ Design Direction Layout: Mirror HashiCorp — two major verticals (Infrastructure Lifecycle / Security Lifecycle) with gradient blocks. (BUT DON'T MOCK!!) if we need more than infra and security than add. Change names too like is Sec doesn't match! Interaction: Each product card expands to reveal quickstart + GitHub. Documentation Theme: Dark mode first, monospace code, gradient accent. Product Icons: Simple line-icons (planet rings, orbits, hexagons).

Celara – Landing Hero & Product Section EXAMPLE
```typescript
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowRight, Shield, ServerCog, Database, Network, LineChart, KeyRound, Layers, Globe, GitBranch } from "lucide-react";

// Brand tokens
const brand = {
  orbitBlue: "#4C6FFF",
  plasmaViolet: "#6B3DF4",
  deepSpace: "#0A0E29",
  nebulaPink: "#F05AFF",
  white: "#FFFFFF",
  teal: "#2DD4BF",
  gray: "#9CA3AF",
};

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
    <div className="min-h-screen w-full bg-[radial-gradient(1200px_800px_at_70%_-20%,rgba(75,0,130,0.25),transparent),radial-gradient(900px_600px_at_-10%_10%,rgba(76,111,255,0.25),transparent)] bg-[#0A0E29] text-white">
      {/* Nav */}
      <header className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-[#4C6FFF] to-[#F05AFF]" />
          <span className="font-semibold tracking-wide">Celara</span>
        </div>
        <nav className="hidden items-center gap-6 md:flex">
          <a className="text-sm text-gray-300 hover:text-white" href="/products">Products</a>
          <a className="text-sm text-gray-300 hover:text-white" href="/open">Open Source</a>
          <a className="text-sm text-gray-300 hover:text-white" href="/runnode">RunNode Cloud</a>
          <a className="text-sm text-gray-300 hover:text-white" href="/docs">Docs</a>
        </nav>
        <div className="flex items-center gap-3">
          <Button variant="secondary" className="bg-white/10 hover:bg-white/20">GitHub</Button>
          <Button className="bg-gradient-to-r from-[#4C6FFF] to-[#F05AFF] text-white hover:opacity-90">Launch Cloud</Button>
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
            <Button className="bg-gradient-to-r from-[#4C6FFF] to-[#6B3DF4]">Explore Products<ArrowRight className="ml-2 h-4 w-4"/></Button>
            <Button variant="outline" className="border-white/20 bg-transparent text-white hover:bg-white/5">Read the Docs</Button>
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
```

Hero + tagline

Two lifecycle panels (renamed to Operations Lifecycle and Security & Governance) with gradient headers

A product grid for NodeQuick, ChainWatch, ChainETL, SecurityKit, DAOForm, ValidatorHub, plus RunNode Cloud & Celara Network

Tailwind + shadcn-ready structure and lucide icons

If you want it as a Next.js page, we can paste it straight into app/page.tsx.

Stack pick (fast + HashiCorp vibe)

Monorepo (Turborepo)

apps/web – Next.js (App Router) + Tailwind + shadcn/ui + MDX for marketing & product pages

apps/docs – Nextra (Next.js-based) for docs at developer.celara.dev (superb MDX, versioning, search)

packages/ui – shared UI tokens/components (buttons, cards, gradients, icons)

Hosting: Vercel (web & docs); Cloudflare proxy fine later.

Content: MDX + Contentlayer for product pages; GitHub Actions for preview builds.

Design tokens: colors you specified (Orbit Blue, Plasma Violet, Deep Space, Nebula Pink, White) baked into Tailwind.

File map

```yaml
celara/
├─ apps/
│  ├─ web/            # marketing
│  │  ├─ app/
│  │  │  ├─ page.tsx        # use the canvas component here
│  │  │  └─ products/[id]/page.mdx
│  │  └─ components/
│  └─ docs/           # Nextra docs
│     ├─ pages/
│     │  ├─ index.mdx
│     │  ├─ nodequick/
│     │  ├─ chainwatch/
│     │  └─ ...
├─ packages/ui/       # shadcn components, tokens, icons
└─ turbo.json
```

Domain + routes

celara.dev → apps/web

developer.celara.dev → apps/docs

/products, /runnode, /open, /network reserved as you outlined.

here’s what each deliverable will look and feel like, plus the file/URL shape so you can picture it clearly.

Product pages (MDX) w/ Quickstart + GitHub “expand”

Where: apps/web/app/products/[slug]/page.mdx
URL: /products/nodequick, /products/chainwatch, etc.

Visual:

Hero block (name, one-line tagline, gradient bar).

Two-column body:

Left: overview, features bullets, architecture diagram (image slot).

Right: sticky “Actions” card with GitHub, Docs, Try in Cloud buttons.

Expandable Quickstart cards embedded mid-page:

Collapsed: shows title + 1-line summary.

Expanded: code block (bash/yaml/ts), copy-button, optional tabs (AWS/GCP/Azure).

Content pattern (per product):

What it is (2–3 sentences)

Why it matters (3 bullets)

Quickstart (expandable card; 3–6 steps with copyable code)

Deeper links (Docs sections, examples)

Compatibility (chains, clouds)

License & GitHub (badges)

Example blocks you’ll see:

Card title: “Quickstart (Terraform)” → expands to init/apply commands.

Card title: “Kubernetes via Helm” → expands to helm install ….

Card title: “Programmatic (Python SDK)” → expands to minimal snippet.

Brand color tokens & gradients

Where: packages/ui/tailwind.config.ts + packages/ui/styles.css
Usage: classes like bg-orbit, from-orbit to-nebula.

Tokens (names → hex):

--celara-orbit: #4C6FFF; (Orbit Blue)

--celara-plasma: #6B3DF4; (Plasma Violet)

--celara-deepspace: #0A0E29; (Deep Space)

--celara-nebula: #F05AFF; (Nebula Pink)

--celara-white: #FFFFFF; (White)

Accent neutrals for cards/borders (--celara-ink-400, --celara-ink-600)

Gradient presets:

Operations: bg-gradient-to-r from-orbit to-plasma

Security/Gov: bg-gradient-to-r from-amber-500 to-nebula (mapped into brand scale)

Neutral platform: from-ink-700 to-ink-500

Outcome: consistent gradients for headers, card rails, and icons; easy one-class reuse across the site.

Convert the canvas component → Next.js App Router page

Where: apps/web/app/layout.tsx and apps/web/app/page.tsx

Layout (global):

Sticky top nav (Logo + Products/Open Source/RunNode/Docs).

Page container: max-w-7xl, generous breathing room, dark background (Deep Space).

Footer w/ links + © Celara.

Home page (your canvas component):

Hero band with badge “Infrastructure for Decentralized Systems”

Two Lifecycle panels (Operations, Security & Governance) with gradient headers and product “pills”

Celara Tools grid: 6 OSS + 2 platform items (each card has a gradient top bar + icon)

Behavior:

Cards are links to /products/[slug].

Buttons: “Explore Products” → /products; “Read the Docs” → https://developer.celara.dev.

Nextra docs skeleton (developer.celara.dev)

Where: apps/docs/
URL: developer.celara.dev

Left sidebar tree (first pass):
```yaml
Intro
  • What is Celara?
  • Architecture
  • Roadmap & Versions
NodeQuick
  • Install
  • Providers
  • Modules & Examples
  • CI/CD
ChainWatch
  • Setup
  • Metrics Reference
  • Dashboards
SecurityKit
  • CLI
  • Keys & Secrets
  • Audits & CI
DAOForm
  • Syntax
  • Templates
  • Deploy Targets
```
Top navigation: “Intro • NodeQuick • ChainWatch • SecurityKit • DAOForm”
Theme: Dark-first; code blocks with copy; built-in search; version dropdown later.

Each section landing page includes:

Short description

Badges: OSS license, GitHub stars, latest release

“Quickstart” (same steps as product page but docs-centric)

Links to examples and reference pages

MDX style:

Admonitions (Tip, Note, Warning)

Tabs for cloud/chain variants

Auto-generated TOC on the right