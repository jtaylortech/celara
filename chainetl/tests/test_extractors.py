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
