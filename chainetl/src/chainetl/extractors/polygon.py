"""Polygon blockchain extractor."""

from chainetl.extractors.evm import EVMExtractor


class PolygonExtractor(EVMExtractor):
    """Extract data from Polygon PoS."""

    def __init__(self, rpc_url: str) -> None:
        super().__init__(rpc_url, chain="polygon")
