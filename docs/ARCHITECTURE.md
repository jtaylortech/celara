# Architecture

## How the Products Fit Together

```
┌──────────────────────────────────────────────────┐
│                   Celara Suite                    │
├──────────┬──────────┬──────────┬────────┬────────┤
│ ChainETL │ ChainOps │ChainWatch│Security│DAOForm │
│          │          │          │  Kit   │        │
│ Extract  │ Deploy   │ Monitor  │ Secure │ Govern │
│ data     │ infra    │ nodes    │ nodes  │ DAOs   │
└────┬─────┴────┬─────┴────┬─────┴───┬────┴───┬────┘
     │          │          │         │        │
     ▼          ▼          ▼         ▼        ▼
  EVM RPC    Terraform  Prometheus  RPC     YAML
  Nodes      + AWS      Metrics    Checks  Config
```

## Shared Patterns

All five products follow the same conventions:

- **Python 3.11+** with type hints and mypy strict
- **Pydantic** for data models and validation
- **Typer** for CLI interfaces
- **Structured logging** with structlog
- **Ruff** for linting
- **Pytest** for testing
- **Hatchling** for packaging

## EVM Extractor Pattern

ChainETL, ChainWatch, and SecurityKit all talk to EVM nodes via JSON-RPC. They share the same approach:

1. A base `EVMExtractor` / `EVMExporter` class handles the RPC calls
2. Chain-specific classes are thin wrappers that set the chain name
3. Adding a new EVM chain is a 3-line file

```python
# Example: adding Optimism to ChainETL
from chainetl.extractors.evm import EVMExtractor

class OptimismExtractor(EVMExtractor):
    def __init__(self, rpc_url: str) -> None:
        super().__init__(rpc_url, chain="optimism")
```

## Data Flow

### ChainETL
```
RPC Node → EVMExtractor → Block/Transaction/Log models → Loader (Postgres or JSONL)
```

### ChainWatch
```
RPC Node → EVMExporter → Prometheus Gauges → Grafana Dashboard
```

### SecurityKit
```
RPC Node → Security Checks → Findings (pass/fail/skip) → Report (text/json/markdown)
```

### ChainOps
```
chainops.yaml → Terraform Templates → AWS Infrastructure
```

### DAOForm
```
dao.yaml → GovernanceEngine → Proposals/Votes → YAML Persistence
```

## API

ChainETL includes a FastAPI REST API for querying blockchain data over HTTP:

```
chainetl serve --port 8000
# GET /chains/ethereum/blocks/18000000
# GET /chains/ethereum/blocks/latest
# GET /chains/ethereum/blocks/18000000/transactions
# GET /chains/ethereum/blocks/18000000/full
```

Auto-generated OpenAPI docs at `/docs` when running.
