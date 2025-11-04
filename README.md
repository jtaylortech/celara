# Celara

**Infrastructure for Decentralized Systems**

> Modular, open-source primitives that professionalize how decentralized systems are built, monitored, and secured.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Website](https://img.shields.io/badge/web-celara.dev-4C6FFF)](https://celara.dev)

---

## 🎯 What is Celara?

Celara is the **HashiCorp of Web3** — a unified suite of infrastructure tools for blockchain validators, RPCs, and DAOs. From deployment to monitoring to governance automation.

**The Problem:** Blockchain infrastructure today mirrors cloud infrastructure circa 2012 — powerful, chaotic, and highly manual.

**The Solution:** Celara brings DevOps discipline to decentralized systems through five core products:

| Product | Purpose | Status |
|---------|---------|--------|
| **[ChainOps](docs/products/chainops.md)** | Infrastructure-as-Code for validators | Planning |
| **[ChainWatch](docs/products/chainwatch.md)** | Observability for decentralized systems | Planning |
| **[SecurityKit](docs/products/securitykit.md)** | Automated security for node operators | Planning |
| **[ChainETL](docs/products/chainetl.md)** | Blockchain data pipelines | Planning |
| **[DAOForm](docs/products/daoform.md)** | Governance-as-Code | Planning |

---

## 🚀 Quick Start

### Marketing Site (This Repo)

```bash
cd web
npm install
npm run dev
```

Visit **http://localhost:3000**

### Product Repos (Coming Soon)

Each product will have its own repository with CLI, docs, and deployment templates.

---

## 📚 Documentation

- **[Brand DNA](docs/CELARA-DNA.md)** - Complete brand, design system, and positioning
- **[Product Architecture](docs/strategy/product-architecture.md)** - Three-pillar strategy and product suite
- **[Business Model](docs/strategy/business-model.md)** - Monetization framework and pricing
- **[GTM Strategy](docs/strategy/gtm-playbook.md)** - Go-to-market motion and growth levers
- **[Phase Map](docs/strategy/phase-map.md)** - 2025-2026 roadmap and milestones
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to Celara

---

## 🏗️ Repository Structure

```
celara-homepage/
├── web/                    # Next.js marketing site
│   ├── app/               # App Router pages
│   ├── components/ui/     # shadcn/ui components
│   └── public/            # Static assets
├── docs/                  # Documentation
│   ├── products/          # Product-specific docs
│   ├── strategy/          # Business & GTM docs
│   └── architecture/      # Technical architecture
└── .github/               # GitHub templates & workflows
```

---

## 🎨 Design System

**Brand Colors:**
```css
--orbit: #4C6FFF      /* Orbit Blue (primary) */
--plasma: #6B3DF4     /* Plasma Violet (secondary) */
--nebula: #F05AFF     /* Nebula Pink (accent) */
--teal: #2DD4BF       /* Teal (success) */
--deepspace: #0A0E29  /* Deep Space (dark bg) */
```

**Stack:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS v4
- shadcn/ui components
- Lucide React icons

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code of conduct
- Development setup
- Contribution workflow
- Design guidelines

---

## 📍 Roadmap

**Q1 2025:** Foundation & OSS Launch
- ChainOps v1.0 (Solana + Ethereum templates)
- ChainWatch Alpha (metrics exporters)
- SecurityKit Agent (baseline security)

**Q3 2025:** Integration & Commercial Readiness
- ChainOps Pro (managed control plane)
- ChainWatch SaaS (public dashboards)
- SecurityKit Vault integration

**Q1 2026:** Data & Governance Layer
- ChainETL launch
- DAOForm alpha
- Celara Cloud (unified console)

See [Phase Map](docs/strategy/phase-map.md) for full timeline.

---

## 🔗 Links

- **Website:** [celara.dev](https://celara.dev) (coming soon)
- **Docs:** [docs.celara.dev](https://docs.celara.dev) (coming soon)
- **GitHub:** [@celara](https://github.com/celara) (coming soon)
- **Discord:** [discord.gg/celara](https://discord.gg/celara) (coming soon)

---

## 📄 License

Apache 2.0 - See [LICENSE](LICENSE) for details.

Open-core model: Core primitives are open-source; managed cloud offerings are commercial.

---

**Built with ⚡ by [JT](https://github.com/jtaylortech) at TaylorTech**
