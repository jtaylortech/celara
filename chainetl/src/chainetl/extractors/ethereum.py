"""Ethereum blockchain extractor."""

from chainetl.extractors.evm import EVMExtractor


class EthereumExtractor(EVMExtractor):
    """Extract data from Ethereum mainnet."""

    def __init__(self, rpc_url: str) -> None:
        super().__init__(rpc_url, chain="ethereum")
