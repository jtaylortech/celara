"""Tests for exporters."""

from unittest.mock import MagicMock, patch

import pytest

from chainwatch.exporters.ethereum import EthereumExporter


@pytest.fixture
def mock_rpc_responses():
    """Mock RPC responses."""
    return {
        "eth_syncing": {"jsonrpc": "2.0", "id": 1, "result": False},
        "eth_blockNumber": {"jsonrpc": "2.0", "id": 1, "result": "0x1234567"},
        "net_peerCount": {"jsonrpc": "2.0", "id": 1, "result": "0x19"},
        "eth_gasPrice": {"jsonrpc": "2.0", "id": 1, "result": "0x3b9aca00"},
        "web3_clientVersion": {"jsonrpc": "2.0", "id": 1, "result": "Geth/v1.13.0"},
    }


def test_ethereum_exporter_init():
    """Test exporter initialization."""
    exporter = EthereumExporter("https://eth.llamarpc.com")
    assert exporter.rpc_url == "https://eth.llamarpc.com"


@patch("chainwatch.exporters.ethereum.httpx.Client")
def test_collect_sync_status_synced(mock_client_class, mock_rpc_responses):
    """Test collecting sync status when node is synced."""
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    def mock_post(url, json):
        method = json["method"]
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_rpc_responses[method]
        return mock_resp

    mock_client.post.side_effect = mock_post

    exporter = EthereumExporter("https://test.rpc")
    exporter._collect_sync_status()

    # Verify RPC calls were made
    assert mock_client.post.call_count >= 1


@patch("chainwatch.exporters.ethereum.httpx.Client")
def test_collect_peer_count(mock_client_class, mock_rpc_responses):
    """Test collecting peer count."""
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    mock_resp = MagicMock()
    mock_resp.json.return_value = mock_rpc_responses["net_peerCount"]
    mock_client.post.return_value = mock_resp

    exporter = EthereumExporter("https://test.rpc")
    exporter._collect_peer_count()

    mock_client.post.assert_called_once()


@patch("chainwatch.exporters.ethereum.httpx.Client")
def test_collect_gas_price(mock_client_class, mock_rpc_responses):
    """Test collecting gas price."""
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    mock_resp = MagicMock()
    mock_resp.json.return_value = mock_rpc_responses["eth_gasPrice"]
    mock_client.post.return_value = mock_resp

    exporter = EthereumExporter("https://test.rpc")
    exporter._collect_gas_price()

    mock_client.post.assert_called_once()
