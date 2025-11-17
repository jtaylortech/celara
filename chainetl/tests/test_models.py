"""Tests for models."""

from chainetl.models.block import Block


def test_block_from_rpc_minimal() -> None:
    """Block.from_rpc should correctly parse minimal RPC block data."""

    rpc_data = {
        "number": "0x10",  # 16
        "hash": "0x" + "a" * 64,
        "parentHash": "0x" + "b" * 64,
        "timestamp": "0x5f5e100",  # 100000000
        "transactions": ["0xdeadbeef"],
    }

    block = Block.from_rpc(rpc_data)

    assert block.number == 16
    assert block.hash.startswith("0x")
    assert block.parent_hash.startswith("0x")
    assert block.timestamp == int("0x5f5e100", 16)
    assert block.transactions == ["0xdeadbeef"]
