"""EVM node metrics exporter.

Works with any EVM-compatible chain: Ethereum, Base, Polygon, Arbitrum.
"""

from typing import Any

import httpx
from prometheus_client import Gauge, Info

# Metrics (labeled by chain)
node_info = Info("chainwatch_node", "Node information")
sync_status = Gauge(
    "chainwatch_sync_status", "Sync status (1=synced, 0=syncing)", ["chain"]
)
current_block = Gauge(
    "chainwatch_current_block", "Current block number", ["chain"]
)
highest_block = Gauge(
    "chainwatch_highest_block", "Highest known block number", ["chain"]
)
peer_count = Gauge(
    "chainwatch_peer_count", "Connected peers", ["chain"]
)
gas_price_gwei = Gauge(
    "chainwatch_gas_price_gwei", "Gas price in gwei", ["chain"]
)


class EVMExporter:
    """Collects Prometheus metrics from any EVM node."""

    def __init__(self, rpc_url: str, chain: str = "ethereum") -> None:
        self.rpc_url = rpc_url
        self.chain = chain
        self.client = httpx.Client(timeout=10.0)

    def _rpc_call(
        self, method: str, params: list[Any] | None = None
    ) -> dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": 1,
        }
        resp = self.client.post(self.rpc_url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def collect(self) -> None:
        """Collect all metrics."""
        self._collect_sync_status()
        self._collect_peer_count()
        self._collect_gas_price()
        self._collect_node_info()

    def _collect_sync_status(self) -> None:
        result = self._rpc_call("eth_syncing")
        syncing = result.get("result")

        if syncing is False:
            sync_status.labels(chain=self.chain).set(1)
            block_result = self._rpc_call("eth_blockNumber")
            block_num = int(block_result.get("result", "0x0"), 16)
            current_block.labels(chain=self.chain).set(block_num)
            highest_block.labels(chain=self.chain).set(block_num)
        elif isinstance(syncing, dict):
            sync_status.labels(chain=self.chain).set(0)
            current_block.labels(chain=self.chain).set(
                int(syncing.get("currentBlock", "0x0"), 16)
            )
            highest_block.labels(chain=self.chain).set(
                int(syncing.get("highestBlock", "0x0"), 16)
            )

    def _collect_peer_count(self) -> None:
        result = self._rpc_call("net_peerCount")
        count = int(result.get("result", "0x0"), 16)
        peer_count.labels(chain=self.chain).set(count)

    def _collect_gas_price(self) -> None:
        result = self._rpc_call("eth_gasPrice")
        price_wei = int(result.get("result", "0x0"), 16)
        gas_price_gwei.labels(chain=self.chain).set(price_wei / 1e9)

    def _collect_node_info(self) -> None:
        result = self._rpc_call("web3_clientVersion")
        client_version = result.get("result", "unknown")
        node_info.info({
            "client_version": str(client_version),
            "chain": self.chain,
        })
