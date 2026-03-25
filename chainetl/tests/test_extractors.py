"""Test extractors."""

import pytest

from chainetl.extractors.base_l2 import BaseL2Extractor
from chainetl.extractors.ethereum import EthereumExtractor

# --- Mocked Ethereum extractor tests ---

@pytest.fixture
def mock_extractor(monkeypatch) -> EthereumExtractor:
    """Create Ethereum extractor with mocked RPC."""
    extractor = EthereumExtractor.__new__(EthereumExtractor)

    class FakeRPC:
        def call(self, method: str, params: list) -> dict | str | None:
            if method == "eth_getBlockByNumber":
                block_hex = params[0]
                block_num = int(block_hex, 16)
                if block_num >= 999999999999:
                    return None
                return {
                    "number": block_hex,
                    "hash": "0x" + "a" * 64,
                    "parentHash": "0x" + "b" * 64,
                    "timestamp": hex(1695000000),
                    "transactions": [],
                }
            if method == "eth_blockNumber":
                return hex(20000000)
            return None

    extractor.rpc = FakeRPC()
    return extractor


def test_extract_block(mock_extractor: EthereumExtractor) -> None:
    """Test extracting a block."""
    block = mock_extractor.extract_block(18000000)
    assert block.number == 18000000
    assert block.hash.startswith("0x")
    assert len(block.hash) == 66
    assert block.timestamp > 0


def test_extract_latest_block_number(mock_extractor: EthereumExtractor) -> None:
    """Test getting latest block number."""
    latest = mock_extractor.extract_latest_block_number()
    assert latest > 18000000


def test_extract_invalid_block(mock_extractor: EthereumExtractor) -> None:
    """Test extracting invalid block."""
    with pytest.raises(ValueError, match="Block .* not found"):
        mock_extractor.extract_block(999999999999)


def test_extract_blocks_batch(mock_extractor: EthereumExtractor) -> None:
    """Test extracting multiple blocks in a batch."""
    blocks = mock_extractor.extract_blocks(18000000, 18000002)
    assert len(blocks) == 3
    assert blocks[0].number == 18000000
    assert blocks[1].number == 18000001
    assert blocks[2].number == 18000002
    for block in blocks:
        assert block.hash.startswith("0x")
        assert len(block.hash) == 66
        assert block.timestamp > 0


def test_extract_blocks_invalid_range(mock_extractor: EthereumExtractor) -> None:
    """Test extracting blocks with invalid range (start > end)."""
    with pytest.raises(ValueError, match="start_block .* must be <= end_block"):
        mock_extractor.extract_blocks(100, 50)


# --- Mocked Base L2 extractor tests ---

@pytest.fixture
def mock_base_extractor() -> BaseL2Extractor:
    """Create Base L2 extractor with mocked RPC."""
    extractor = BaseL2Extractor.__new__(BaseL2Extractor)

    class FakeRPC:
        def call(self, method: str, params: list) -> dict | str | None:
            if method == "eth_getBlockByNumber":
                block_hex = params[0]
                return {
                    "number": block_hex,
                    "hash": "0x" + "c" * 64,
                    "parentHash": "0x" + "d" * 64,
                    "timestamp": hex(1695000000),
                    "transactions": [],
                }
            if method == "eth_blockNumber":
                return hex(20000000)
            return None

    extractor.rpc = FakeRPC()
    return extractor


def test_base_chain_name(mock_base_extractor: BaseL2Extractor) -> None:
    """Test Base L2 chain name property."""
    assert mock_base_extractor.chain_name == "base"


def test_base_extract_block(mock_base_extractor: BaseL2Extractor) -> None:
    """Test extracting a block from Base L2."""
    block = mock_base_extractor.extract_block(10000000)
    assert block.number == 10000000
    assert block.hash.startswith("0x")
    assert len(block.hash) == 66
    assert block.timestamp > 0


def test_base_extract_latest_block_number(mock_base_extractor: BaseL2Extractor) -> None:
    """Test getting latest block number from Base L2."""
    latest = mock_base_extractor.extract_latest_block_number()
    assert latest > 10000000


def test_base_extract_blocks_batch(mock_base_extractor: BaseL2Extractor) -> None:
    """Test extracting multiple blocks from Base L2."""
    blocks = mock_base_extractor.extract_blocks(10000000, 10000002)
    assert len(blocks) == 3
    assert blocks[0].number == 10000000
    assert blocks[1].number == 10000001
    assert blocks[2].number == 10000002
    for block in blocks:
        assert block.hash.startswith("0x")
        assert len(block.hash) == 66
        assert block.timestamp > 0


def test_base_extract_blocks_invalid_range(mock_base_extractor: BaseL2Extractor) -> None:
    """Test extracting blocks with invalid range on Base L2."""
    with pytest.raises(ValueError, match="start_block .* must be <= end_block"):
        mock_base_extractor.extract_blocks(100, 50)


def test_ethereum_chain_name(mock_extractor: EthereumExtractor) -> None:
    """Test Ethereum chain name property."""
    assert mock_extractor.chain_name == "ethereum"
