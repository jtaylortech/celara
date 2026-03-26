"""Ethereum node metrics exporter (backward-compatible wrapper)."""

from chainwatch.exporters.evm import EVMExporter


class EthereumExporter(EVMExporter):
    """Ethereum-specific exporter."""

    def __init__(self, rpc_url: str) -> None:
        super().__init__(rpc_url, chain="ethereum")
