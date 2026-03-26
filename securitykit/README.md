# SecurityKit

Automated security scanning for blockchain nodes. No SSH required.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

---

## What it does

Scan your EVM node's RPC endpoint for common security misconfigurations. Get findings with severity levels and remediation steps. Exit code 1 on failures — drop it into CI.

## Quick Start

```bash
cd securitykit
uv sync

# Scan a node
uv run securitykit scan --rpc-url https://eth.llamarpc.com

# JSON output for CI/CD
uv run securitykit scan --rpc-url https://eth.llamarpc.com --output json
```

## Security Checks

| ID | Check | Severity |
|----|-------|----------|
| SK-001 | RPC endpoint reachable | Critical |
| SK-002 | No unlocked accounts | Critical |
| SK-003 | Mining disabled | Medium |
| SK-004 | Minimum peer count | High |
| SK-005 | Node fully synced | High |

## Example Output

```
Scanning https://eth.llamarpc.com...

  ✅ [SK-001] RPC endpoint is reachable
     Node responded: Geth/v1.13.0

  ✅ [SK-002] No unlocked accounts
     eth_accounts returned empty list

  ✅ [SK-003] Mining is disabled
     eth_mining returned false

  ✅ [SK-004] Peer count healthy
     25 peers connected

  ✅ [SK-005] Node is fully synced
     eth_syncing returned false (synced)

Results: 5 passed, 0 failed, 0 skipped
```

## Adding Custom Checks

```python
from securitykit.models import Finding, Severity, Status

def check_my_rule(rpc_url: str) -> Finding:
    # Your check logic here
    return Finding(
        rule_id="SK-100",
        title="My custom check",
        severity=Severity.HIGH,
        status=Status.PASS,
        detail="All good",
    )
```

## License

Apache 2.0 — See [LICENSE](LICENSE)

---

Part of [Celara](https://celara.dev) — open-source DevOps tooling for decentralized systems.
