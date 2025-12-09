"""Ethereum node metrics exporter."""

from typing import Any

import httpx
from prometheus_client import Gauge, Info

# Node info
node_info = Info("chainwatch_node", "Ethereum node information")

# Sync metrics
sync_status = Gauge("chainwatch_sync_status", "Node sync status (1=synced, 0=syncing)")
current_block = Gauge("chainwatch_current_block", "Current block number")
highest_block = Gauge("chainwatch_highest_block", "Highest known block number")

# Peer metrics
peer_count = Gauge("chainwatch_peer_count", "Number of connected peers")

# Gas metrics
gas_price_gwei = Gauge("chainwatch_gas_price_gwei", "Current gas price in gwei")


class EthereumExporter:
    """Collects metrics from Ethereum execution client."""

    def __init__(self, rpc_url: str) -> None:
        self.rpc_url = rpc_url
        self.client = httpx.Client(timeout=10.0)

    def _rpc_call(self, method: str, params: list[Any] | None = None) -> dict[str, Any]:
        """Make JSON-RPC call."""
        payload = {"jsonrpc": "2.0", "method": method, "params": params or [], "id": 1}
        resp = self.client.post(self.rpc_url, json=payload)
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    def collect(self) -> None:
        """Collect all metrics."""
        self._collect_sync_status()
        self._collect_peer_count()
        self._collect_gas_price()
        self._collect_node_info()

    def _collect_sync_status(self) -> None:
        """Collect sync status metrics."""
        result = self._rpc_call("eth_syncing")
        syncing = result.get("result")

        if syncing is False:
            # Node is synced
            sync_status.set(1)
            block_result = self._rpc_call("eth_blockNumber")
            block_num = int(block_result.get("result", "0x0"), 16)
            current_block.set(block_num)
            highest_block.set(block_num)
        elif isinstance(syncing, dict):
            # Node is syncing
            sync_status.set(0)
            current_block.set(int(syncing.get("currentBlock", "0x0"), 16))
            highest_block.set(int(syncing.get("highestBlock", "0x0"), 16))

    def _collect_peer_count(self) -> None:
        """Collect peer count."""
        result = self._rpc_call("net_peerCount")
        count = int(result.get("result", "0x0"), 16)
        peer_count.set(count)

    def _collect_gas_price(self) -> None:
        """Collect current gas price."""
        result = self._rpc_call("eth_gasPrice")
        price_wei = int(result.get("result", "0x0"), 16)
        price_gwei = price_wei / 1e9
        gas_price_gwei.set(price_gwei)

    def _collect_node_info(self) -> None:
        """Collect node client info."""
        result = self._rpc_call("web3_clientVersion")
        client_version = result.get("result", "unknown")
        node_info.info({"client_version": str(client_version), "chain": "ethereum"})
