"""Test extractors."""

import pytest

from chainetl.extractors.arbitrum import ArbitrumExtractor
from chainetl.extractors.base_l2 import BaseL2Extractor
from chainetl.extractors.ethereum import EthereumExtractor
from chainetl.extractors.evm import EVMExtractor
from chainetl.extractors.polygon import PolygonExtractor

# ERC-20 Transfer signature
TRANSFER_SIG = (
    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
)


class FakeRPC:
    """Mock RPC client for testing."""

    def call(self, method: str, params: list) -> dict | str | None:
        if method == "eth_getBlockByNumber":
            block_num = int(params[0], 16)
            if block_num >= 999999999999:
                return None
            full_txs = params[1] if len(params) > 1 else False
            tx_hash = "0x" + "f" * 64
            if full_txs:
                txs: list = [{
                    "hash": tx_hash,
                    "blockNumber": params[0],
                    "blockHash": "0x" + "a" * 64,
                    "transactionIndex": "0x0",
                    "from": "0x" + "1" * 40,
                    "to": "0x" + "2" * 40,
                    "value": "0x0",
                    "input": "0x",
                    "gas": "0x5208",
                    "gasPrice": "0x3b9aca00",
                    "nonce": "0x0",
                }]
            else:
                txs = []
            return {
                "number": params[0],
                "hash": "0x" + "a" * 64,
                "parentHash": "0x" + "b" * 64,
                "timestamp": hex(1695000000),
                "transactions": txs,
            }
        if method == "eth_blockNumber":
            return hex(20000000)
        if method == "eth_getTransactionReceipt":
            return {
                "transactionHash": params[0],
                "blockNumber": "0x10",
                "blockHash": "0x" + "a" * 64,
                "logs": [{
                    "address": "0x" + "c" * 40,
                    "topics": [
                        TRANSFER_SIG,
                        "0x" + "0" * 24 + "1" * 40,
                        "0x" + "0" * 24 + "2" * 40,
                    ],
                    "data": "0x" + "0" * 63 + "64",
                    "logIndex": "0x0",
                    "transactionHash": params[0],
                    "blockNumber": "0x10",
                    "blockHash": "0x" + "a" * 64,
                }],
            }
        return None

    def close(self) -> None:
        pass


def _make_extractor(
    cls: type[EVMExtractor], **kwargs: str
) -> EVMExtractor:
    """Create extractor with mocked RPC."""
    extractor = cls.__new__(cls)
    extractor.rpc = FakeRPC()
    extractor._chain = kwargs.get(
        "chain", cls.__name__.replace("Extractor", "").lower()
    )
    return extractor


@pytest.fixture
def eth() -> EthereumExtractor:
    return _make_extractor(EthereumExtractor, chain="ethereum")


@pytest.fixture
def base_ext() -> BaseL2Extractor:
    return _make_extractor(BaseL2Extractor, chain="base")


@pytest.fixture
def polygon() -> PolygonExtractor:
    return _make_extractor(PolygonExtractor, chain="polygon")


@pytest.fixture
def arbitrum() -> ArbitrumExtractor:
    return _make_extractor(ArbitrumExtractor, chain="arbitrum")


# --- Chain names ---

def test_ethereum_chain_name(eth: EthereumExtractor) -> None:
    assert eth.chain_name == "ethereum"


def test_base_chain_name(base_ext: BaseL2Extractor) -> None:
    assert base_ext.chain_name == "base"


def test_polygon_chain_name(polygon: PolygonExtractor) -> None:
    assert polygon.chain_name == "polygon"


def test_arbitrum_chain_name(arbitrum: ArbitrumExtractor) -> None:
    assert arbitrum.chain_name == "arbitrum"


# --- Block extraction ---

def test_extract_block(eth: EthereumExtractor) -> None:
    block = eth.extract_block(18000000)
    assert block.number == 18000000
    assert block.hash.startswith("0x")
    assert len(block.hash) == 66
    assert block.timestamp > 0


def test_extract_latest_block_number(eth: EthereumExtractor) -> None:
    assert eth.extract_latest_block_number() > 18000000


def test_extract_invalid_block(eth: EthereumExtractor) -> None:
    with pytest.raises(ValueError, match="Block .* not found"):
        eth.extract_block(999999999999)


def test_extract_blocks_batch(eth: EthereumExtractor) -> None:
    blocks = eth.extract_blocks(18000000, 18000002)
    assert len(blocks) == 3
    assert blocks[0].number == 18000000
    assert blocks[2].number == 18000002


def test_extract_blocks_invalid_range(eth: EthereumExtractor) -> None:
    with pytest.raises(ValueError, match="start_block .* must be <= end_block"):
        eth.extract_blocks(100, 50)


# --- Cross-chain ---

def test_base_extract_block(base_ext: BaseL2Extractor) -> None:
    assert base_ext.extract_block(10000000).number == 10000000


def test_polygon_extract_block(polygon: PolygonExtractor) -> None:
    assert polygon.extract_block(50000000).number == 50000000


def test_arbitrum_extract_block(arbitrum: ArbitrumExtractor) -> None:
    assert arbitrum.extract_block(200000000).number == 200000000


# --- Composite extraction (evm.py coverage) ---

def test_extract_block_with_transactions(eth: EthereumExtractor) -> None:
    block, txs = eth.extract_block_with_transactions(18000000)
    assert block.number == 18000000
    assert len(txs) == 1
    assert txs[0].hash == "0x" + "f" * 64


def test_extract_transaction_receipt(eth: EthereumExtractor) -> None:
    receipt = eth.extract_transaction_receipt("0x" + "f" * 64)
    assert receipt["transactionHash"] == "0x" + "f" * 64
    assert len(receipt["logs"]) == 1


def test_extract_receipt_not_found(eth: EthereumExtractor) -> None:
    """Receipt returns None from RPC → should raise."""
    # Override RPC to return None for receipts
    class NoneReceiptRPC(FakeRPC):
        def call(self, method: str, params: list) -> dict | str | None:
            if method == "eth_getTransactionReceipt":
                return None
            return super().call(method, params)

    eth.rpc = NoneReceiptRPC()
    with pytest.raises(ValueError, match="Receipt .* not found"):
        eth.extract_transaction_receipt("0xdead")


def test_extract_logs_from_receipt(eth: EthereumExtractor) -> None:
    receipt = eth.extract_transaction_receipt("0x" + "f" * 64)
    logs = eth.extract_logs_from_receipt(receipt)
    assert len(logs) == 1
    assert logs[0].address == "0x" + "c" * 40


def test_extract_transaction_with_logs(eth: EthereumExtractor) -> None:
    receipt, logs, transfers = eth.extract_transaction_with_logs(
        "0x" + "f" * 64
    )
    assert len(logs) == 1
    assert len(transfers) == 1
    assert transfers[0].token_standard == "ERC-20"


def test_extract_block_with_full_data(eth: EthereumExtractor) -> None:
    block, txs, logs, transfers = eth.extract_block_with_full_data(18000000)
    assert block.number == 18000000
    assert len(txs) == 1
    assert len(logs) == 1
    assert len(transfers) == 1


def test_close(eth: EthereumExtractor) -> None:
    eth.close()  # Should not raise
