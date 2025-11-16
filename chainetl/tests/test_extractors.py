"""Test extractors."""

import pytest

from chainetl.extractors.ethereum import EthereumExtractor


@pytest.fixture
def extractor() -> EthereumExtractor:
    """Create Ethereum extractor."""
    return EthereumExtractor(rpc_url="https://eth.llamarpc.com")


def test_extract_block(extractor: EthereumExtractor) -> None:
    """Test extracting a block."""
    block = extractor.extract_block(18000000)

    assert block.number == 18000000
    assert block.hash.startswith("0x")
    assert len(block.hash) == 66  # 0x + 64 hex chars
    assert block.timestamp > 0


def test_extract_latest_block_number(extractor: EthereumExtractor) -> None:
    """Test getting latest block number."""
    latest = extractor.extract_latest_block_number()
    assert latest > 18000000  # Should be higher than this old block


def test_extract_invalid_block(extractor: EthereumExtractor) -> None:
    """Test extracting invalid block."""
    with pytest.raises(ValueError, match="Block .* not found"):
        extractor.extract_block(999999999999)


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
