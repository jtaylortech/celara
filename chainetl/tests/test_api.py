"""Tests for the REST API."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from chainetl.api import app
from chainetl.models.block import Block
from chainetl.models.transaction import Transaction

client = TestClient(app)


class FakeExtractor:
    def __init__(self, rpc_url: str, chain: str) -> None:
        self.chain = chain

    def extract_latest_block_number(self) -> int:
        return 20000000

    def extract_block(self, n: int) -> Block:
        return Block(
            number=n, hash="0x" + "a" * 64,
            parent_hash="0x" + "b" * 64,
            timestamp=1700000000, transactions=["0x" + "f" * 64],
        )

    def extract_block_with_transactions(self, n: int):
        block = self.extract_block(n)
        tx = Transaction.from_rpc({
            "hash": "0x" + "f" * 64, "blockNumber": hex(n),
            "blockHash": "0x" + "a" * 64, "transactionIndex": "0x0",
            "from": "0x" + "1" * 40, "to": "0x" + "2" * 40,
            "value": "0x0", "input": "0x", "gas": "0x5208",
            "gasPrice": "0x3b9aca00", "nonce": "0x0",
        })
        return block, [tx]

    def close(self) -> None:
        pass


@patch("chainetl.api.EVMExtractor", FakeExtractor)
def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "chains" in r.json()


@patch("chainetl.api.EVMExtractor", FakeExtractor)
def test_list_chains():
    r = client.get("/chains")
    assert "ethereum" in r.json()


@patch("chainetl.api.EVMExtractor", FakeExtractor)
def test_chain_info():
    r = client.get("/chains/ethereum")
    assert r.status_code == 200
    assert r.json()["latest_block"] == 20000000


@patch("chainetl.api.EVMExtractor", FakeExtractor)
def test_get_block():
    r = client.get("/chains/ethereum/blocks/18000000")
    assert r.status_code == 200
    assert r.json()["number"] == 18000000
    assert r.json()["transaction_count"] == 1


@patch("chainetl.api.EVMExtractor", FakeExtractor)
def test_get_block_transactions():
    r = client.get("/chains/ethereum/blocks/18000000/transactions")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["from_address"] == "0x" + "1" * 40


@patch("chainetl.api.EVMExtractor", FakeExtractor)
def test_get_latest_block():
    r = client.get("/chains/ethereum/blocks/latest")
    assert r.status_code == 200
    assert r.json()["number"] == 20000000


def test_unsupported_chain():
    r = client.get("/chains/solana")
    assert r.status_code == 400
    assert "Unsupported" in r.json()["detail"]
