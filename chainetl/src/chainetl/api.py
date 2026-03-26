"""ChainETL REST API.

FastAPI service for querying blockchain data in real-time.
No database required — queries RPC directly.

Usage:
    uvicorn chainetl.api:app --reload
    # or
    chainetl serve --port 8000
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from chainetl.extractors.evm import EVMExtractor

app = FastAPI(
    title="ChainETL API",
    description="Query blockchain data from any EVM chain",
    version="0.2.0",
)

# Default RPC endpoints
RPCS: dict[str, str] = {
    "ethereum": "https://eth.llamarpc.com",
    "base": "https://mainnet.base.org",
    "polygon": "https://polygon-rpc.com",
    "arbitrum": "https://arb1.arbitrum.io/rpc",
}


def _get_extractor(chain: str) -> EVMExtractor:
    if chain not in RPCS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported chain: {chain}. Supported: {', '.join(RPCS)}",
        )
    return EVMExtractor(RPCS[chain], chain=chain)


# --- Response models ---


class BlockResponse(BaseModel):
    number: int
    hash: str
    parent_hash: str
    timestamp: int
    transaction_count: int


class TransactionResponse(BaseModel):
    hash: str
    block_number: int
    from_address: str
    to_address: str | None
    value: int
    gas: int


class ChainInfoResponse(BaseModel):
    chain: str
    latest_block: int
    rpc_url: str


# --- Routes ---


@app.get("/")
def root() -> dict:
    return {
        "name": "ChainETL API",
        "version": "0.2.0",
        "docs": "/docs",
        "chains": list(RPCS.keys()),
    }


@app.get("/chains")
def list_chains() -> list[str]:
    return list(RPCS.keys())


@app.get("/chains/{chain}")
def chain_info(chain: str) -> ChainInfoResponse:
    ext = _get_extractor(chain)
    try:
        latest = ext.extract_latest_block_number()
        return ChainInfoResponse(
            chain=chain, latest_block=latest, rpc_url=RPCS[chain]
        )
    finally:
        ext.close()


@app.get("/chains/{chain}/blocks/latest")
def get_latest_block(chain: str) -> BlockResponse:
    ext = _get_extractor(chain)
    try:
        latest = ext.extract_latest_block_number()
        block = ext.extract_block(latest)
        return BlockResponse(
            number=block.number,
            hash=block.hash,
            parent_hash=block.parent_hash,
            timestamp=block.timestamp,
            transaction_count=len(block.transactions),
        )
    finally:
        ext.close()


@app.get("/chains/{chain}/blocks/{block_number}")
def get_block(chain: str, block_number: int) -> BlockResponse:
    ext = _get_extractor(chain)
    try:
        block = ext.extract_block(block_number)
        return BlockResponse(
            number=block.number,
            hash=block.hash,
            parent_hash=block.parent_hash,
            timestamp=block.timestamp,
            transaction_count=len(block.transactions),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    finally:
        ext.close()


@app.get("/chains/{chain}/blocks/{block_number}/transactions")
def get_block_transactions(
    chain: str, block_number: int
) -> list[TransactionResponse]:
    ext = _get_extractor(chain)
    try:
        _, txs = ext.extract_block_with_transactions(block_number)
        return [
            TransactionResponse(
                hash=tx.hash,
                block_number=tx.block_number,
                from_address=tx.from_address,
                to_address=tx.to_address,
                value=tx.value,
                gas=tx.gas,
            )
            for tx in txs
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    finally:
        ext.close()
