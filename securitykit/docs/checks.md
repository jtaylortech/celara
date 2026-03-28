# Security Checks

Each check runs against a node's JSON-RPC endpoint. No SSH, no agents.

## Check Reference

### SK-001: RPC Reachability (Critical)
**Method**: `web3_clientVersion`
**Pass**: Node responds with client version string.
**Fail**: No response — node is down or URL is wrong.

### SK-002: Unlocked Accounts (Critical)
**Method**: `eth_accounts`
**Pass**: Empty list returned.
**Fail**: One or more accounts are unlocked. This is the #1 cause of fund loss on validator nodes — anyone with RPC access can sign transactions.
**Fix**: Lock all accounts. Never run validators with unlocked accounts.

### SK-003: Admin API Exposure (Critical)
**Method**: `admin_nodeInfo`
**Pass**: Method not available (returns error or no response).
**Fail**: Admin namespace is accessible. Allows peer manipulation, data export, and node control.
**Fix**: Disable admin API namespace. Never expose it publicly.

### SK-004: Debug API Exposure (High)
**Method**: `debug_traceBlockByNumber`
**Pass**: Method not available.
**Fail**: Debug namespace is accessible. Can leak internal state and cause DoS via expensive trace operations.
**Fix**: Disable debug API namespace in production.

### SK-005: Mining Status (Medium)
**Method**: `eth_mining`
**Pass**: Returns `false`.
**Fail**: Mining is enabled. Should be disabled unless this is an intentional miner node.
**Fix**: Disable mining unless required.

### SK-006: Peer Count (High)
**Method**: `net_peerCount`
**Pass**: ≥3 peers connected.
**Fail**: Fewer than 3 peers. Indicates network isolation, firewall misconfiguration, or bootnode issues.
**Fix**: Check firewall rules. Verify bootnodes. Ensure P2P port (30303) is open.

### SK-007: Sync Status (High)
**Method**: `eth_syncing`
**Pass**: Returns `false` (fully synced).
**Fail**: Node is still syncing. Should not validate or serve RPC until sync is complete.
**Fix**: Wait for sync to complete.

### SK-008: Chain ID (Medium)
**Method**: `eth_chainId`
**Pass**: Returns a known chain ID (1=Ethereum, 137=Polygon, 42161=Arbitrum, 8453=Base).
**Fail**: N/A (informational check).
**Purpose**: Catches testnet/mainnet misconfigurations.

## Adding Custom Checks

Every check is a function with signature `(rpc_url: str) -> Finding`:

```python
from securitykit.models import Finding, Severity, Status

def check_my_rule(rpc_url: str) -> Finding:
    # Your logic here
    return Finding(
        rule_id="CUSTOM-001",
        title="My check",
        severity=Severity.HIGH,
        status=Status.PASS,
        detail="All good",
        remediation="Fix instructions if failed",
    )
```

Add it to `ALL_CHECKS` in `checks.py` — the CLI and audit runner pick it up automatically.
