"""Test extractors."""

import pytest

from chainetl.extractors.arbitrum import ArbitrumExtractor
from chainetl.extractors.base_l2 import BaseL2Extractor
from chainetl.extractors.ethereum import EthereumExtractor
from chainetl.extractors.evm import EVMExtractor
from chainetl.extractors.polygon import PolygonExtractor


class FakeRPC:
    """Mock RPC client for testing."""

    def call(self, method: str, params: list) -> dict | str | None:
        if method == "eth_getBlockByNumber":
            block_num = int(params[0], 16)
            if block_num >= 999999999999:
                return None
            return {
                "number": params[0],
                "hash": "0x" + "a" * 64,
                "parentHash": "0x" + "b" * 64,
                "timestamp": hex(1695000000),
                "transactions": [],
            }
        if method == "eth_blockNumber":
            return hex(20000000)
        return None

    def close(self) -> None:
        pass


def _make_extractor(cls: type[EVMExtractor], **kwargs) -> EVMExtractor:
    """Create extractor with mocked RPC."""
    extractor = cls.__new__(cls)
    extractor.rpc = FakeRPC()
    extractor._chain = kwargs.get("chain", cls.__name__.replace("Extractor", "").lower())
    return extractor


@pytest.fixture
def eth_extractor() -> EthereumExtractor:
    return _make_extractor(EthereumExtractor, chain="ethereum")


@pytest.fixture
def base_extractor() -> BaseL2Extractor:
    return _make_extractor(BaseL2Extractor, chain="base")


@pytest.fixture
def polygon_extractor() -> PolygonExtractor:
    return _make_extractor(PolygonExtractor, chain="polygon")


@pytest.fixture
def arbitrum_extractor() -> ArbitrumExtractor:
    return _make_extractor(ArbitrumExtractor, chain="arbitrum")


# --- Chain name tests ---

def test_ethereum_chain_name(eth_extractor: EthereumExtractor) -> None:
    assert eth_extractor.chain_name == "ethereum"


def test_base_chain_name(base_extractor: BaseL2Extractor) -> None:
    assert base_extractor.chain_name == "base"


def test_polygon_chain_name(polygon_extractor: PolygonExtractor) -> None:
    assert polygon_extractor.chain_name == "polygon"


def test_arbitrum_chain_name(arbitrum_extractor: ArbitrumExtractor) -> None:
    assert arbitrum_extractor.chain_name == "arbitrum"


# --- Core extraction tests (using Ethereum, applies to all EVM) ---

def test_extract_block(eth_extractor: EthereumExtractor) -> None:
    block = eth_extractor.extract_block(18000000)
    assert block.number == 18000000
    assert block.hash.startswith("0x")
    assert len(block.hash) == 66
    assert block.timestamp > 0


def test_extract_latest_block_number(eth_extractor: EthereumExtractor) -> None:
    assert eth_extractor.extract_latest_block_number() > 18000000


def test_extract_invalid_block(eth_extractor: EthereumExtractor) -> None:
    with pytest.raises(ValueError, match="Block .* not found"):
        eth_extractor.extract_block(999999999999)


def test_extract_blocks_batch(eth_extractor: EthereumExtractor) -> None:
    blocks = eth_extractor.extract_blocks(18000000, 18000002)
    assert len(blocks) == 3
    assert blocks[0].number == 18000000
    assert blocks[2].number == 18000002
    for block in blocks:
        assert block.hash.startswith("0x")
        assert block.timestamp > 0


def test_extract_blocks_invalid_range(eth_extractor: EthereumExtractor) -> None:
    with pytest.raises(ValueError, match="start_block .* must be <= end_block"):
        eth_extractor.extract_blocks(100, 50)


# --- Cross-chain extraction (verify all chains work identically) ---

def test_base_extract_block(base_extractor: BaseL2Extractor) -> None:
    block = base_extractor.extract_block(10000000)
    assert block.number == 10000000
    assert block.hash.startswith("0x")


def test_polygon_extract_block(polygon_extractor: PolygonExtractor) -> None:
    block = polygon_extractor.extract_block(50000000)
    assert block.number == 50000000
    assert block.hash.startswith("0x")


def test_arbitrum_extract_block(arbitrum_extractor: ArbitrumExtractor) -> None:
    block = arbitrum_extractor.extract_block(200000000)
    assert block.number == 200000000
    assert block.hash.startswith("0x")


def test_close(eth_extractor: EthereumExtractor) -> None:
    eth_extractor.close()  # Should not raise
