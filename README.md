# Celara

**DevOps tooling for decentralized systems**

Open-source infrastructure for blockchain validators, node operators, and DAOs.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Website](https://img.shields.io/badge/web-celara.dev-5C6FFF)](https://celara.dev)

---

## Products

| Product | Purpose | Status |
|---------|---------|--------|
| **[ChainETL](chainetl/)** | Blockchain data pipelines | In Development |
| **[ChainOps](chainops/)** | Infrastructure-as-Code for validators | In Development |
| **[ChainWatch](chainwatch/)** | Observability for decentralized systems | In Development |
| **[SecurityKit](securitykit/)** | Automated security for node operators | Planning |
| **[DAOForm](daoform/)** | Governance-as-Code | Planning |

---

## Quick Start

### Marketing Site

```bash
cd web
npm install
npm run dev
```

Visit **http://localhost:3000**

### ChainETL

```bash
cd chainetl
uv sync
uv run chainetl sync --chain ethereum --start-block 18000000 --count 10
```

### ChainWatch

```bash
cd chainwatch
uv sync
uv run chainwatch exporter --chain ethereum
```

---

## Repository Structure

```
celara-homepage/
├── chainetl/          # Blockchain data pipelines
├── chainops/          # Infrastructure-as-Code for validators
├── chainwatch/        # Observability for decentralized systems
├── securitykit/       # Automated security for node operators
├── daoform/           # Governance-as-Code
├── web/               # Next.js marketing site
└── docs/              # Documentation
```

---

## Documentation

- **[Design System](docs/DESIGN_SYSTEM.md)** - Brand colors, typography, components
- **[Product Architecture](docs/strategy/product-architecture.md)** - Product suite overview
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Fork the repo, then:
git checkout -b feature/your-feature
# Make changes
git commit -m "feat: your feature"
git push origin feature/your-feature
# Open a PR
```

---

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.

---

**Built by [Jarred](https://github.com/jtaylortech) & [Kofi](https://github.com/kofikwarba)**
