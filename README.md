# Celara

Open-source DevOps tooling for decentralized systems.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Website](https://img.shields.io/badge/web-celara.dev-5C6FFF)](https://celara.dev)
[![Tests](https://img.shields.io/badge/tests-134%20passing-brightgreen)](https://github.com/jtaylortech/celara-homepage)

---

## Products

| Product | What it does | Tests |
|---------|-------------|-------|
| **[ChainETL](chainetl/)** | Blockchain data pipelines — 4 EVM chains, Postgres + JSONL, REST API | 74 |
| **[ChainOps](chainops/)** | Infrastructure-as-Code — Terraform validator deployment for ETH + SOL | 12 |
| **[ChainWatch](chainwatch/)** | Observability — Prometheus metrics exporter, Grafana dashboard | 9 |
| **[SecurityKit](securitykit/)** | Security — 8 RPC-based node checks, audit reports | 21 |
| **[DAOForm](daoform/)** | Governance — proposals, weighted voting, YAML persistence | 18 |

## Install

```bash
pip install chainetl chainops chainwatch securitykit daoform
```

## Quick Start

```bash
# Extract blockchain data
chainetl sync --chain ethereum --start-block 18000000 --count 10

# Deploy a validator
chainops init ethereum --network mainnet && chainops deploy

# Monitor a node
chainwatch exporter --chain ethereum --port 9100

# Security scan
securitykit scan --rpc-url https://eth.llamarpc.com

# DAO governance
daoform init --name MyDAO && daoform validate

# Start the REST API
chainetl serve --port 8000
```

## Documentation

Full docs at **[celara.dev/docs](https://celara.dev/docs)**

- [ChainETL](https://celara.dev/docs/chainetl) — extraction, models, CLI, adding chains
- [ChainOps](https://celara.dev/docs/chainops) — deployment, costs, Terraform
- [ChainWatch](https://celara.dev/docs/chainwatch) — metrics, Grafana, alerts
- [SecurityKit](https://celara.dev/docs/securitykit) — checks, reports, custom rules
- [DAOForm](https://celara.dev/docs/daoform) — governance model, SDK, persistence
- [REST API](https://celara.dev/docs/api) — endpoints, response models, client examples

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — See [LICENSE](LICENSE)

---

**Built by [Jarred](https://github.com/jtaylortech) & [Kofi](https://github.com/kofikwarba)**
