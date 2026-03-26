"""Tests for the REST API."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from chainetl.api import app
from chainetl.models.block import Block
from chainetl.models.log import Log
from chainetl.models.token_transfer import TokenTransfer
from chainetl.models.transaction import Transaction

client = TestClient(app)

TX_HASH = "0x" + "f" * 64


class FakeExtractor:
    def __init__(self, rpc_url: str, chain: str) -> None:
        self.chain = chain

    def extract_latest_block_number(self) -> int:
        return 20000000

    def extract_block(self, n: int) -> Block:
        return Block(
            number=n, hash="0x" + "a" * 64,
            parent_hash="0x" + "b" * 64,
            timestamp=1700000000, transactions=[TX_HASH],
        )

    def extract_block_with_transactions(self, n: int):
        block = self.extract_block(n)
        tx = Transaction.from_rpc({
            "hash": TX_HASH, "blockNumber": hex(n),
            "blockHash": "0x" + "a" * 64,
            "transactionIndex": "0x0",
            "from": "0x" + "1" * 40, "to": "0x" + "2" * 40,
            "value": "0x0", "input": "0x", "gas": "0x5208",
            "gasPrice": "0x3b9aca00", "nonce": "0x0",
        })
        return block, [tx]

    def extract_block_with_full_data(self, n: int):
        block, txs = self.extract_block_with_transactions(n)
        log = Log(
            address="0x" + "c" * 40, topics=[], data="0x",
            log_index=0, transaction_hash=TX_HASH, block_number=n,
        )
        transfer = TokenTransfer(
            transaction_hash=TX_HASH, log_index=0,
            block_number=n, token_address="0x" + "c" * 40,
            token_standard="ERC-20",
            from_address="0x" + "1" * 40,
            to_address="0x" + "2" * 40, value="1000",
        )
        return block, txs, [log], [transfer]

    def close(self) -> None:
        pass


P = "chainetl.api.EVMExtractor"


@patch(P, FakeExtractor)
def test_health():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert "X-Request-Id" in r.headers
    assert "X-Response-Time" in r.headers


@patch(P, FakeExtractor)
def test_chain_info():
    r = client.get("/chains/ethereum")
    assert r.status_code == 200
    assert r.json()["latest_block"] == 20000000
    assert r.json()["chain"] == "ethereum"


@patch(P, FakeExtractor)
def test_get_block():
    r = client.get("/chains/ethereum/blocks/18000000")
    assert r.status_code == 200
    d = r.json()
    assert d["number"] == 18000000
    assert d["chain"] == "ethereum"
    assert d["transaction_count"] == 1


@patch(P, FakeExtractor)
def test_get_latest_block():
    r = client.get("/chains/ethereum/blocks/latest")
    assert r.status_code == 200
    assert r.json()["number"] == 20000000


@patch(P, FakeExtractor)
def test_get_transactions():
    r = client.get("/chains/ethereum/blocks/18000000/transactions")
    assert r.status_code == 200
    txs = r.json()
    assert len(txs) == 1
    assert txs[0]["from_address"] == "0x" + "1" * 40
    assert txs[0]["value"] == "0"


@patch(P, FakeExtractor)
def test_get_block_full():
    r = client.get("/chains/ethereum/blocks/18000000/full")
    assert r.status_code == 200
    d = r.json()
    assert d["number"] == 18000000
    assert len(d["transactions"]) == 1
    assert d["logs_count"] == 1
    assert len(d["token_transfers"]) == 1
    assert d["token_transfers"][0]["token_standard"] == "ERC-20"


def test_unsupported_chain():
    r = client.get("/chains/solana")
    assert r.status_code == 400
    assert "unsupported_chain" in str(r.json())


@patch(P, FakeExtractor)
def test_cors_headers():
    r = client.options(
        "/chains/ethereum",
        headers={"Origin": "http://localhost:3000"},
    )
    assert "access-control-allow-origin" in r.headers
