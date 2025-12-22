"""Tests for Phase 5: Transaction & Log Extraction."""

from chainetl.models.log import Log
from chainetl.models.token_transfer import TokenTransfer
from chainetl.models.transaction import Transaction
from chainetl.utils.token_parser import (
    is_erc20_transfer,
    is_erc721_transfer,
    parse_token_transfer,
    parse_token_transfers_from_logs,
)


def test_transaction_from_rpc_legacy() -> None:
    """Transaction.from_rpc should correctly parse legacy transaction data."""
    rpc_data = {
        "hash": "0x" + "a" * 64,
        "blockNumber": "0x10",  # 16
        "blockHash": "0x" + "b" * 64,
        "transactionIndex": "0x0",
        "from": "0x" + "c" * 40,
        "to": "0x" + "d" * 40,
        "value": "0xde0b6b3a7640000",  # 1 ETH in wei
        "input": "0x",
        "gas": "0x5208",  # 21000
        "gasPrice": "0x3b9aca00",  # 1 gwei
        "nonce": "0x5",
        "type": "0x0",  # Legacy
        "chainId": "0x1",  # Ethereum mainnet
        "v": "0x25",
        "r": "0x" + "e" * 64,
        "s": "0x" + "f" * 64,
    }

    tx = Transaction.from_rpc(rpc_data)

    assert tx.hash == "0x" + "a" * 64
    assert tx.block_number == 16
    assert tx.from_address == "0x" + "c" * 40
    assert tx.to_address == "0x" + "d" * 40
    assert tx.value == 1000000000000000000  # 1 ETH
    assert tx.gas == 21000
    assert tx.gas_price == 1000000000  # 1 gwei
    assert tx.nonce == 5
    assert tx.transaction_type == 0
    assert tx.chain_id == 1


def test_transaction_from_rpc_eip1559() -> None:
    """Transaction.from_rpc should correctly parse EIP-1559 transaction data."""
    rpc_data = {
        "hash": "0x" + "a" * 64,
        "blockNumber": "0x100",
        "blockHash": "0x" + "b" * 64,
        "transactionIndex": "0x1",
        "from": "0x" + "c" * 40,
        "to": "0x" + "d" * 40,
        "value": "0x0",
        "input": "0xa9059cbb",  # Some function call
        "gas": "0x30d40",  # 200000
        "maxFeePerGas": "0x77359400",  # 2 gwei
        "maxPriorityFeePerGas": "0x3b9aca00",  # 1 gwei
        "nonce": "0xa",
        "type": "0x2",  # EIP-1559
        "chainId": "0x1",
        "v": "0x1",
        "r": "0x" + "e" * 64,
        "s": "0x" + "f" * 64,
    }

    tx = Transaction.from_rpc(rpc_data)

    assert tx.transaction_type == 2
    assert tx.max_fee_per_gas == 2000000000  # 2 gwei
    assert tx.max_priority_fee_per_gas == 1000000000  # 1 gwei
    assert tx.gas_price is None  # EIP-1559 doesn't use gasPrice


def test_transaction_from_rpc_contract_creation() -> None:
    """Transaction.from_rpc should handle contract creation (to=None)."""
    rpc_data = {
        "hash": "0x" + "a" * 64,
        "blockNumber": "0x10",
        "blockHash": "0x" + "b" * 64,
        "transactionIndex": "0x0",
        "from": "0x" + "c" * 40,
        "to": None,  # Contract creation
        "value": "0x0",
        "input": "0x606060",  # Contract bytecode
        "gas": "0x100000",
        "gasPrice": "0x3b9aca00",
        "nonce": "0x0",
        "type": "0x0",
        "chainId": "0x1",
        "v": "0x25",
        "r": "0x" + "e" * 64,
        "s": "0x" + "f" * 64,
    }

    tx = Transaction.from_rpc(rpc_data)

    assert tx.to_address is None


def test_token_transfer_from_erc20_log() -> None:
    """TokenTransfer.from_erc20_log should correctly parse ERC-20 Transfer events."""
    log_data = {
        "address": "0x" + "a" * 40,  # Token contract
        "topics": [
            # Transfer signature
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "0x" + "0" * 24 + "b" * 40,  # from (padded)
            "0x" + "0" * 24 + "c" * 40,  # to (padded)
        ],
        "data": "0x00000000000000000000000000000000000000000000000000000000000003e8",  # 1000
        "logIndex": "0x5",
    }

    transfer = TokenTransfer.from_erc20_log(
        log_data, transaction_hash="0x" + "d" * 64, block_number=100
    )

    assert transfer.token_address == "0x" + "a" * 40
    assert transfer.token_standard == "ERC-20"
    assert transfer.from_address == "0x" + "b" * 40
    assert transfer.to_address == "0x" + "c" * 40
    assert transfer.value == "1000"
    assert transfer.transaction_hash == "0x" + "d" * 64
    assert transfer.block_number == 100
    assert transfer.log_index == 5


def test_token_transfer_from_erc721_log() -> None:
    """TokenTransfer.from_erc721_log should correctly parse ERC-721 Transfer events."""
    log_data = {
        "address": "0x" + "a" * 40,
        "topics": [
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "0x" + "0" * 24 + "b" * 40,  # from
            "0x" + "0" * 24 + "c" * 40,  # to
            "0x" + "0" * 63 + "7b",  # tokenId = 123
        ],
        "data": "0x",
        "logIndex": "0x3",
    }

    transfer = TokenTransfer.from_erc721_log(
        log_data, transaction_hash="0x" + "d" * 64, block_number=200
    )

    assert transfer.token_standard == "ERC-721"
    assert transfer.from_address == "0x" + "b" * 40
    assert transfer.to_address == "0x" + "c" * 40
    assert transfer.value == "123"  # Token ID
    assert transfer.log_index == 3


def test_is_erc20_transfer() -> None:
    """is_erc20_transfer should identify ERC-20 Transfer events (3 topics)."""
    log = Log(
        address="0x" + "a" * 40,
        topics=[
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "0x" + "b" * 64,
            "0x" + "c" * 64,
        ],
        data="0x1234",
        log_index=0,
        transaction_hash="0x" + "d" * 64,
        block_number=100,
        block_hash="0x" + "e" * 64,
    )

    assert is_erc20_transfer(log) is True


def test_is_erc721_transfer() -> None:
    """is_erc721_transfer should identify ERC-721 Transfer events (4 topics)."""
    log = Log(
        address="0x" + "a" * 40,
        topics=[
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "0x" + "b" * 64,
            "0x" + "c" * 64,
            "0x" + "d" * 64,  # tokenId
        ],
        data="0x",
        log_index=0,
        transaction_hash="0x" + "e" * 64,
        block_number=100,
        block_hash="0x" + "f" * 64,
    )

    assert is_erc721_transfer(log) is True


def test_is_erc20_vs_erc721_distinction() -> None:
    """is_erc20_transfer and is_erc721_transfer should be mutually exclusive."""
    # ERC-20: 3 topics
    erc20_log = Log(
        address="0x" + "a" * 40,
        topics=[
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "0x" + "b" * 64,
            "0x" + "c" * 64,
        ],
        data="0x1234",
        log_index=0,
        transaction_hash="0x" + "d" * 64,
        block_number=100,
        block_hash="0x" + "e" * 64,
    )

    # ERC-721: 4 topics
    erc721_log = Log(
        address="0x" + "a" * 40,
        topics=[
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "0x" + "b" * 64,
            "0x" + "c" * 64,
            "0x" + "d" * 64,
        ],
        data="0x",
        log_index=1,
        transaction_hash="0x" + "e" * 64,
        block_number=100,
        block_hash="0x" + "f" * 64,
    )

    # ERC-20 check
    assert is_erc20_transfer(erc20_log) is True
    assert is_erc721_transfer(erc20_log) is False

    # ERC-721 check
    assert is_erc721_transfer(erc721_log) is True
    assert is_erc20_transfer(erc721_log) is False


def test_parse_token_transfer_erc20() -> None:
    """parse_token_transfer should parse ERC-20 transfers."""
    log = Log(
        address="0x" + "a" * 40,
        topics=[
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "0x" + "0" * 24 + "b" * 40,
            "0x" + "0" * 24 + "c" * 40,
        ],
        data="0x" + "0" * 63 + "64",  # 100
        log_index=5,
        transaction_hash="0x" + "d" * 64,
        block_number=100,
        block_hash="0x" + "e" * 64,
    )

    transfer = parse_token_transfer(log, "0x" + "d" * 64, 100)

    assert transfer is not None
    assert transfer.token_standard == "ERC-20"
    assert transfer.value == "100"


def test_parse_token_transfer_erc721() -> None:
    """parse_token_transfer should parse ERC-721 transfers."""
    log = Log(
        address="0x" + "a" * 40,
        topics=[
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "0x" + "0" * 24 + "b" * 40,
            "0x" + "0" * 24 + "c" * 40,
            "0x" + "0" * 63 + "7b",  # tokenId = 123
        ],
        data="0x",
        log_index=3,
        transaction_hash="0x" + "d" * 64,
        block_number=200,
        block_hash="0x" + "e" * 64,
    )

    transfer = parse_token_transfer(log, "0x" + "d" * 64, 200)

    assert transfer is not None
    assert transfer.token_standard == "ERC-721"
    assert transfer.value == "123"


def test_parse_token_transfer_non_transfer() -> None:
    """parse_token_transfer should return None for non-Transfer events."""
    log = Log(
        address="0x" + "a" * 40,
        topics=[
            "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925",  # Approval event
            "0x" + "b" * 64,
        ],
        data="0x",
        log_index=0,
        transaction_hash="0x" + "c" * 64,
        block_number=100,
        block_hash="0x" + "d" * 64,
    )

    transfer = parse_token_transfer(log, "0x" + "c" * 64, 100)

    assert transfer is None


def test_parse_token_transfers_from_logs_mixed() -> None:
    """parse_token_transfers_from_logs should filter and parse multiple transfers."""
    logs = [
        # ERC-20 Transfer
        Log(
            address="0x" + "a" * 40,
            topics=[
                "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
                "0x" + "0" * 24 + "b" * 40,
                "0x" + "0" * 24 + "c" * 40,
            ],
            data="0x64",  # 100
            log_index=0,
            transaction_hash="0x" + "d" * 64,
            block_number=100,
            block_hash="0x" + "e" * 64,
        ),
        # Non-Transfer event (should be filtered out)
        Log(
            address="0x" + "a" * 40,
            topics=["0x" + "f" * 64],
            data="0x",
            log_index=1,
            transaction_hash="0x" + "d" * 64,
            block_number=100,
            block_hash="0x" + "e" * 64,
        ),
        # ERC-721 Transfer
        Log(
            address="0x" + "a" * 40,
            topics=[
                "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
                "0x" + "0" * 24 + "b" * 40,
                "0x" + "0" * 24 + "c" * 40,
                "0x7b",  # tokenId = 123
            ],
            data="0x",
            log_index=2,
            transaction_hash="0x" + "d" * 64,
            block_number=100,
            block_hash="0x" + "e" * 64,
        ),
    ]

    transfers = parse_token_transfers_from_logs(logs, "0x" + "d" * 64, 100)

    assert len(transfers) == 2  # Only the 2 Transfer events
    assert transfers[0].token_standard == "ERC-20"
    assert transfers[1].token_standard == "ERC-721"


def test_parse_token_transfers_from_logs_empty() -> None:
    """parse_token_transfers_from_logs should handle empty log lists."""
    transfers = parse_token_transfers_from_logs([], "0x" + "a" * 64, 100)

    assert transfers == []
