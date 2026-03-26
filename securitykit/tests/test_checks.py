"""Tests for security checks."""

from unittest.mock import patch

from securitykit.checks import (
    check_mining_enabled,
    check_peer_count,
    check_rpc_exposed,
    check_sync_status,
    check_unlocked_accounts,
)
from securitykit.models import Severity, Status


def _mock_rpc(return_value):
    """Create a mock for _rpc_call that returns a fixed value."""
    return patch(
        "securitykit.checks._rpc_call", return_value=return_value
    )


def test_rpc_exposed_pass():
    with _mock_rpc({"result": "Geth/v1.13.0"}):
        f = check_rpc_exposed("http://test")
    assert f.status == Status.PASS
    assert f.rule_id == "SK-001"


def test_rpc_exposed_fail():
    with _mock_rpc(None):
        f = check_rpc_exposed("http://test")
    assert f.status == Status.FAIL
    assert f.severity == Severity.CRITICAL


def test_unlocked_accounts_none():
    with _mock_rpc({"result": []}):
        f = check_unlocked_accounts("http://test")
    assert f.status == Status.PASS


def test_unlocked_accounts_found():
    with _mock_rpc({"result": ["0x" + "a" * 40]}):
        f = check_unlocked_accounts("http://test")
    assert f.status == Status.FAIL
    assert f.severity == Severity.CRITICAL


def test_unlocked_accounts_skip():
    with _mock_rpc(None):
        f = check_unlocked_accounts("http://test")
    assert f.status == Status.SKIP


def test_mining_disabled():
    with _mock_rpc({"result": False}):
        f = check_mining_enabled("http://test")
    assert f.status == Status.PASS


def test_mining_enabled():
    with _mock_rpc({"result": True}):
        f = check_mining_enabled("http://test")
    assert f.status == Status.FAIL


def test_peer_count_healthy():
    with _mock_rpc({"result": "0x19"}):  # 25 peers
        f = check_peer_count("http://test")
    assert f.status == Status.PASS
    assert "25" in f.detail


def test_peer_count_low():
    with _mock_rpc({"result": "0x1"}):  # 1 peer
        f = check_peer_count("http://test")
    assert f.status == Status.FAIL


def test_sync_complete():
    with _mock_rpc({"result": False}):
        f = check_sync_status("http://test")
    assert f.status == Status.PASS


def test_sync_in_progress():
    with _mock_rpc({"result": {"currentBlock": "0x100", "highestBlock": "0x200"}}):
        f = check_sync_status("http://test")
    assert f.status == Status.FAIL
