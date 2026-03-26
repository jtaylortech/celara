"""Tests for audit runner."""

from unittest.mock import patch

from securitykit.audit import run_audit
from securitykit.models import Status


def test_run_audit():
    """Audit returns findings for all checks."""
    mock_responses = {
        "web3_clientVersion": {"result": "Geth/v1.13.0"},
        "eth_accounts": {"result": []},
        "eth_mining": {"result": False},
        "net_peerCount": {"result": "0x19"},
        "eth_syncing": {"result": False},
    }

    def fake_rpc(url, method, params=None):
        return mock_responses.get(method)

    with patch("securitykit.checks._rpc_call", side_effect=fake_rpc):
        findings = run_audit("http://test")

    assert len(findings) == 5
    assert all(f.status == Status.PASS for f in findings)
