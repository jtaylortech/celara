"""Additional model tests for transactions and logs."""

from chainetl.models.log import Log
from chainetl.models.transaction import Transaction


def test_transaction_from_rpc_minimal() -> None:
    rpc = {
        "hash": "0x" + "f" * 64,
        "from": "0x" + "1" * 40,
        "to": "0x" + "2" * 40,
        "value": "0x10",
        "gas": "0x5208",
        "gasPrice": "0x3b9aca00",
        "nonce": "0x0",
        "input": "0x",
    }

    tx = Transaction.from_rpc(rpc)
    assert tx.hash.startswith("0x")
    assert tx.value == 16
    assert tx.gas == int("0x5208", 16)


def test_log_from_rpc_minimal() -> None:
    rpc = {
        "address": "0x" + "a" * 40,
        "topics": ["0x" + "0" * 64],
        "data": "0x",
        "logIndex": "0x1",
        "transactionHash": "0x" + "b" * 64,
        "blockNumber": "0x10",
    }

    log = Log.from_rpc(rpc)
    assert log.address.startswith("0x")
    assert log.log_index == 1
    assert log.block_number == 16
