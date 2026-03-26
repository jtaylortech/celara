"""RPC-based security checks for EVM nodes.

These checks run against a node's JSON-RPC endpoint — no SSH required.
They catch the most common misconfigurations that lead to fund loss.
"""

from typing import Any

import httpx

from securitykit.models import Finding, Severity, Status


def _rpc_call(
    url: str, method: str, params: list[Any] | None = None
) -> dict[str, Any] | None:
    """Make a JSON-RPC call. Returns None on failure."""
    try:
        resp = httpx.post(
            url,
            json={"jsonrpc": "2.0", "method": method, "params": params or [], "id": 1},
            timeout=10.0,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def check_rpc_exposed(rpc_url: str) -> Finding:
    """SK-001: Check if RPC is publicly reachable."""
    result = _rpc_call(rpc_url, "web3_clientVersion")
    if result and "result" in result:
        return Finding(
            rule_id="SK-001",
            title="RPC endpoint is reachable",
            severity=Severity.INFO,
            status=Status.PASS,
            detail=f"Node responded: {result['result']}",
        )
    return Finding(
        rule_id="SK-001",
        title="RPC endpoint is unreachable",
        severity=Severity.CRITICAL,
        status=Status.FAIL,
        detail="Node did not respond to web3_clientVersion",
        remediation="Verify RPC URL and network connectivity",
    )


def check_unlocked_accounts(rpc_url: str) -> Finding:
    """SK-002: Check for unlocked accounts (critical vulnerability)."""
    result = _rpc_call(rpc_url, "eth_accounts")
    if result is None:
        return Finding(
            rule_id="SK-002",
            title="Unlocked accounts check",
            severity=Severity.HIGH,
            status=Status.SKIP,
            detail="Could not query eth_accounts",
        )
    accounts = result.get("result", [])
    if accounts:
        return Finding(
            rule_id="SK-002",
            title="Unlocked accounts detected",
            severity=Severity.CRITICAL,
            status=Status.FAIL,
            detail=f"Found {len(accounts)} unlocked account(s)",
            remediation="Lock all accounts. Never run validators with unlocked accounts.",
        )
    return Finding(
        rule_id="SK-002",
        title="No unlocked accounts",
        severity=Severity.CRITICAL,
        status=Status.PASS,
        detail="eth_accounts returned empty list",
    )


def check_mining_enabled(rpc_url: str) -> Finding:
    """SK-003: Check if mining/minting is enabled."""
    result = _rpc_call(rpc_url, "eth_mining")
    if result is None:
        return Finding(
            rule_id="SK-003",
            title="Mining status check",
            severity=Severity.MEDIUM,
            status=Status.SKIP,
            detail="Could not query eth_mining",
        )
    mining = result.get("result", False)
    if mining:
        return Finding(
            rule_id="SK-003",
            title="Mining is enabled",
            severity=Severity.MEDIUM,
            status=Status.FAIL,
            detail="eth_mining returned true",
            remediation="Disable mining unless this is an intentional miner node.",
        )
    return Finding(
        rule_id="SK-003",
        title="Mining is disabled",
        severity=Severity.MEDIUM,
        status=Status.PASS,
        detail="eth_mining returned false",
    )


def check_peer_count(rpc_url: str, min_peers: int = 3) -> Finding:
    """SK-004: Check minimum peer connectivity."""
    result = _rpc_call(rpc_url, "net_peerCount")
    if result is None:
        return Finding(
            rule_id="SK-004",
            title="Peer count check",
            severity=Severity.HIGH,
            status=Status.SKIP,
            detail="Could not query net_peerCount",
        )
    peers = int(result.get("result", "0x0"), 16)
    if peers < min_peers:
        return Finding(
            rule_id="SK-004",
            title="Low peer count",
            severity=Severity.HIGH,
            status=Status.FAIL,
            detail=f"Only {peers} peers (minimum: {min_peers})",
            remediation="Check firewall rules and bootnodes configuration.",
        )
    return Finding(
        rule_id="SK-004",
        title="Peer count healthy",
        severity=Severity.HIGH,
        status=Status.PASS,
        detail=f"{peers} peers connected",
    )


def check_sync_status(rpc_url: str) -> Finding:
    """SK-005: Check if node is fully synced."""
    result = _rpc_call(rpc_url, "eth_syncing")
    if result is None:
        return Finding(
            rule_id="SK-005",
            title="Sync status check",
            severity=Severity.HIGH,
            status=Status.SKIP,
            detail="Could not query eth_syncing",
        )
    syncing = result.get("result")
    if syncing is False:
        return Finding(
            rule_id="SK-005",
            title="Node is fully synced",
            severity=Severity.HIGH,
            status=Status.PASS,
            detail="eth_syncing returned false (synced)",
        )
    return Finding(
        rule_id="SK-005",
        title="Node is still syncing",
        severity=Severity.HIGH,
        status=Status.FAIL,
        detail="Node has not finished syncing",
        remediation="Wait for sync to complete before validating.",
    )


# All checks in execution order
ALL_CHECKS = [
    check_rpc_exposed,
    check_unlocked_accounts,
    check_mining_enabled,
    check_peer_count,
    check_sync_status,
]
