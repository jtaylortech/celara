"""Base L2 blockchain extractor."""

from chainetl.extractors.evm import EVMExtractor


class BaseL2Extractor(EVMExtractor):
    """Extract data from Base L2."""

    def __init__(self, rpc_url: str) -> None:
        super().__init__(rpc_url, chain="base")
