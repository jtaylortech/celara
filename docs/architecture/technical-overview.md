# Celara Technical Architecture

**Last Updated:** November 4, 2025

## System Overview

Celara is a modular, open-core infrastructure platform for decentralized systems. Each product operates independently but integrates seamlessly through shared APIs, data models, and authentication.

---

## Architecture Principles

### 1. Modularity

Each product is independently deployable:
- Separate repositories
- Independent release cycles
- Standalone functionality
- Optional integrations

### 2. Open Core

```
┌─────────────────────────────────────────┐
│           OSS Core Layer                │
│  (CLIs, Templates, Agents, Connectors)  │
└─────────────────────────────────────────┘
                  │
┌─────────────────┼─────────────────┐
│                 │                 │
▼                 ▼                 ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│   SaaS   │  │Enterprise│  │ Advisory │
│  Layer   │  │  Layer   │  │  Layer   │
└──────────┘  └──────────┘  └──────────┘
```

### 3. Cloud-Native

- Containerized (Docker + Kubernetes)
- Serverless where appropriate (Lambda, Cloud Functions)
- Multi-cloud support (AWS, GCP, Azure)
- Infrastructure-as-Code (Terraform, CDK, Pulumi)

### 4. API-First

All products expose REST/GraphQL APIs:
- Versioned endpoints
- OpenAPI specifications
- Rate limiting
- Authentication (OAuth2, API keys)

---

## Product Architecture

### ChainOps

**Stack:**
- **CLI:** TypeScript + Commander.js
- **IaC:** AWS CDK, Terraform, Pulumi
- **Backend:** Node.js + Express
- **Database:** PostgreSQL (state management)
- **Queue:** Redis (job processing)

**Deployment:**
```
User → CLI → API Gateway → Lambda → CDK/Terraform → Cloud Provider
```

---

### ChainWatch

**Stack:**
- **Frontend:** Next.js + React + Tailwind
- **Backend:** FastAPI + Python
- **Metrics:** Prometheus + Grafana
- **Database:** TimescaleDB (time-series)
- **Cache:** Redis

**Data Flow:**
```
Validator → Exporter → Prometheus → TimescaleDB → API → Dashboard
```

---

### SecurityKit

**Stack:**
- **Agent:** Rust (performance + security)
- **Backend:** Go + gRPC
- **Key Vault:** HashiCorp Vault
- **Database:** PostgreSQL
- **Alerting:** PagerDuty, Slack, Discord

**Architecture:**
```
Node → Agent → gRPC → Backend → Vault/KMS
                              ↓
                         Alert Engine
```

---

### ChainETL

**Stack:**
- **Connectors:** Python + asyncio
- **Orchestration:** Airflow / Dagster
- **Transform:** dbt
- **Storage:** S3, Snowflake, BigQuery
- **API:** FastAPI

**Pipeline:**
```
Blockchain RPC → Connector → Transform → Load → Warehouse
                                              ↓
                                         Analytics
```

---

### DAOForm

**Stack:**
- **Frontend:** Next.js + React
- **Backend:** Node.js + Express
- **Database:** PostgreSQL
- **Blockchain:** Web3.js, Anchor (Solana)
- **Integrations:** Snapshot, Gnosis Safe

**Flow:**
```
User → Dashboard → API → Smart Contract → On-Chain Execution
                       ↓
                  Off-Chain Storage
```

---

## Integration Architecture

### Unified Authentication

**OAuth2 + API Keys:**
```typescript
// Shared auth service
const auth = new CelaraAuth({
  provider: 'oauth2',
  scopes: ['chainops:read', 'chainwatch:write'],
});

// Cross-product authentication
const client = new ChainOpsClient({ auth });
const metrics = new ChainWatchClient({ auth });
```

### Shared Data Models

```typescript
// Common types across products
interface Validator {
  id: string;
  chain: 'solana' | 'ethereum' | 'cosmos';
  address: string;
  status: 'active' | 'inactive' | 'delinquent';
  metadata: Record<string, any>;
}

interface Deployment {
  id: string;
  validator: Validator;
  infrastructure: Infrastructure;
  monitoring: MonitoringConfig;
  security: SecurityConfig;
}
```

### Event Bus

```
┌─────────────────────────────────────────┐
│          Event Bus (Kafka/SNS)          │
└─────────────────────────────────────────┘
         │         │         │
    ┌────▼───┐ ┌───▼────┐ ┌─▼──────┐
    │ChainOps│ │ChainWatch│ │SecurityKit│
    └────────┘ └────────┘ └────────┘

Events:
- validator.deployed
- validator.updated
- alert.triggered
- key.rotated
```

---

## Security Architecture

### Defense in Depth

**Layer 1: Network**
- VPC isolation
- Private subnets
- Security groups
- DDoS protection

**Layer 2: Application**
- Input validation
- Rate limiting
- CORS policies
- CSP headers

**Layer 3: Data**
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Key rotation
- Audit logging

**Layer 4: Identity**
- OAuth2 + OIDC
- MFA enforcement
- Role-based access control (RBAC)
- API key rotation

### Secrets Management

```
Application → Vault/KMS → Encrypted Secrets
                        ↓
                   Audit Log
```

---

## Observability

### Metrics

**Prometheus + Grafana:**
- Request latency (p50, p95, p99)
- Error rates
- Throughput
- Resource utilization

### Logging

**Structured Logging (JSON):**
```json
{
  "timestamp": "2025-01-15T14:32:00Z",
  "level": "info",
  "service": "chainops-api",
  "request_id": "abc123",
  "user_id": "user_456",
  "action": "deploy_validator",
  "chain": "solana",
  "duration_ms": 1234
}
```

### Tracing

**OpenTelemetry:**
- Distributed tracing across services
- Request flow visualization
- Performance bottleneck identification

---

## Scalability

### Horizontal Scaling

- Stateless services (scale via replicas)
- Load balancing (ALB, NLB)
- Auto-scaling (CPU/memory thresholds)

### Database Scaling

- Read replicas
- Connection pooling
- Query optimization
- Caching (Redis)

### Cost Optimization

- Spot instances for batch jobs
- Reserved instances for steady-state
- S3 lifecycle policies
- CloudFront CDN

---

## Disaster Recovery

### Backup Strategy

- **Databases:** Daily snapshots, 30-day retention
- **Object Storage:** Cross-region replication
- **Configuration:** Version-controlled IaC

### RTO/RPO Targets

| Tier | RTO | RPO |
|------|-----|-----|
| **Free** | 24h | 24h |
| **Pro** | 4h | 1h |
| **Enterprise** | 1h | 15min |

---

## Development Workflow

### CI/CD Pipeline

```
Git Push → GitHub Actions → Tests → Build → Deploy
                                          ↓
                                    Staging → Production
```

**Stages:**
1. Lint + Type Check
2. Unit Tests
3. Integration Tests
4. Security Scan (Snyk, Trivy)
5. Build Docker Image
6. Deploy to Staging
7. Smoke Tests
8. Deploy to Production

### Environments

- **Development:** Local + Docker Compose
- **Staging:** AWS (isolated account)
- **Production:** AWS (multi-region)

---

## Technology Stack Summary

| Layer | Technologies |
|-------|-------------|
| **Frontend** | Next.js, React, TypeScript, Tailwind CSS |
| **Backend** | Node.js, Python (FastAPI), Go, Rust |
| **Database** | PostgreSQL, TimescaleDB, Redis |
| **Infrastructure** | AWS, Terraform, CDK, Kubernetes |
| **Monitoring** | Prometheus, Grafana, OpenTelemetry |
| **Security** | Vault, KMS, OAuth2, TLS 1.3 |
| **CI/CD** | GitHub Actions, Docker, ArgoCD |

---

## Next Steps

See:
- [Product Architecture](../strategy/product-architecture.md) for product details
- [Business Model](../strategy/business-model.md) for monetization
- [Contributing Guide](../../CONTRIBUTING.md) for development setup
