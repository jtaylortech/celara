"""Test extractors."""

import pytest

from chainetl.extractors.base_l2 import BaseL2Extractor
from chainetl.extractors.ethereum import EthereumExtractor


@pytest.fixture
def extractor() -> EthereumExtractor:
    """Create Ethereum extractor."""
    return EthereumExtractor(rpc_url="https://eth.llamarpc.com")


@pytest.mark.integration
def test_extract_block(extractor: EthereumExtractor) -> None:
    """Test extracting a block."""
    block = extractor.extract_block(18000000)

    assert block.number == 18000000
    assert block.hash.startswith("0x")
    assert len(block.hash) == 66  # 0x + 64 hex chars
    assert block.timestamp > 0


@pytest.mark.integration
def test_extract_latest_block_number(extractor: EthereumExtractor) -> None:
    """Test getting latest block number."""
    latest = extractor.extract_latest_block_number()
    assert latest > 18000000  # Should be higher than this old block


@pytest.mark.integration
def test_extract_invalid_block(extractor: EthereumExtractor) -> None:
    """Test extracting invalid block."""
    with pytest.raises(ValueError, match="Block .* not found"):
        extractor.extract_block(999999999999)


@pytest.mark.integration
def test_extract_blocks_batch(extractor: EthereumExtractor) -> None:
    """Test extracting multiple blocks in a batch."""
    # Extract 3 blocks starting from 18000000
    blocks = extractor.extract_blocks(18000000, 18000002)

    assert len(blocks) == 3
    assert blocks[0].number == 18000000
    assert blocks[1].number == 18000001
    assert blocks[2].number == 18000002

    # Verify each block has valid data
    for block in blocks:
        assert block.hash.startswith("0x")
        assert len(block.hash) == 66
        assert block.timestamp > 0


def test_extract_blocks_invalid_range(extractor: EthereumExtractor) -> None:
    """Test extracting blocks with invalid range (start > end)."""
    with pytest.raises(ValueError, match="start_block .* must be <= end_block"):
        extractor.extract_blocks(100, 50)


@pytest.fixture
def base_extractor() -> BaseL2Extractor:
    """Create Base L2 extractor."""
    return BaseL2Extractor(rpc_url="https://mainnet.base.org")


def test_base_chain_name(base_extractor: BaseL2Extractor) -> None:
    """Test Base L2 chain name property."""
    assert base_extractor.chain_name == "base"


def test_base_extract_block(base_extractor: BaseL2Extractor) -> None:
    """Test extracting a block from Base L2."""
    # Base mainnet started at block 0, test a recent block
    block = base_extractor.extract_block(10000000)

    assert block.number == 10000000
    assert block.hash.startswith("0x")
    assert len(block.hash) == 66  # 0x + 64 hex chars
    assert block.timestamp > 0


def test_base_extract_latest_block_number(base_extractor: BaseL2Extractor) -> None:
    """Test getting latest block number from Base L2."""
    latest = base_extractor.extract_latest_block_number()
    assert latest > 10000000  # Should be higher than this block


def test_base_extract_blocks_batch(base_extractor: BaseL2Extractor) -> None:
    """Test extracting multiple blocks from Base L2."""
    # Extract 3 blocks
    blocks = base_extractor.extract_blocks(10000000, 10000002)

    assert len(blocks) == 3
    assert blocks[0].number == 10000000
    assert blocks[1].number == 10000001
    assert blocks[2].number == 10000002

    # Verify each block has valid data
    for block in blocks:
        assert block.hash.startswith("0x")
        assert len(block.hash) == 66
        assert block.timestamp > 0


def test_base_extract_blocks_invalid_range(base_extractor: BaseL2Extractor) -> None:
    """Test extracting blocks with invalid range on Base L2."""
    with pytest.raises(ValueError, match="start_block .* must be <= end_block"):
        base_extractor.extract_blocks(100, 50)


def test_ethereum_chain_name(extractor: EthereumExtractor) -> None:
    """Test Ethereum chain name property."""
    assert extractor.chain_name == "ethereum"
