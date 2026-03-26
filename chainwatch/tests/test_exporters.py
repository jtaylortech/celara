"""Tests for exporters."""

from unittest.mock import MagicMock

from chainwatch.exporters.ethereum import EthereumExporter
from chainwatch.exporters.evm import EVMExporter

MOCK_RESPONSES = {
    "eth_syncing": {"jsonrpc": "2.0", "id": 1, "result": False},
    "eth_blockNumber": {"jsonrpc": "2.0", "id": 1, "result": "0x1234567"},
    "net_peerCount": {"jsonrpc": "2.0", "id": 1, "result": "0x19"},
    "eth_gasPrice": {"jsonrpc": "2.0", "id": 1, "result": "0x3b9aca00"},
    "web3_clientVersion": {"jsonrpc": "2.0", "id": 1, "result": "Geth/v1.13.0"},
}


def _mock_post(url, json):
    resp = MagicMock()
    resp.json.return_value = MOCK_RESPONSES[json["method"]]
    return resp


def _make_exporter(chain: str = "ethereum") -> EVMExporter:
    """Create exporter with mocked HTTP client."""
    exp = EVMExporter.__new__(EVMExporter)
    exp.rpc_url = "http://test"
    exp.chain = chain
    exp.client = MagicMock()
    exp.client.post.side_effect = _mock_post
    return exp


def test_ethereum_exporter_init():
    exp = EthereumExporter("https://eth.llamarpc.com")
    assert exp.rpc_url == "https://eth.llamarpc.com"
    assert exp.chain == "ethereum"


def test_evm_exporter_chain_label():
    exp = _make_exporter("polygon")
    assert exp.chain == "polygon"


def test_collect_sync_status_synced():
    exp = _make_exporter()
    exp._collect_sync_status()
    assert exp.client.post.call_count >= 1


def test_collect_peer_count():
    exp = _make_exporter()
    exp._collect_peer_count()
    exp.client.post.assert_called_once()


def test_collect_gas_price():
    exp = _make_exporter()
    exp._collect_gas_price()
    exp.client.post.assert_called_once()


def test_collect_node_info():
    exp = _make_exporter()
    exp._collect_node_info()
    exp.client.post.assert_called_once()


def test_collect_all():
    exp = _make_exporter()
    exp.collect()
    assert exp.client.post.call_count >= 4
