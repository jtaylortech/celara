"""Arbitrum blockchain extractor."""

from chainetl.extractors.evm import EVMExtractor


class ArbitrumExtractor(EVMExtractor):
    """Extract data from Arbitrum One."""

    def __init__(self, rpc_url: str) -> None:
        super().__init__(rpc_url, chain="arbitrum")
