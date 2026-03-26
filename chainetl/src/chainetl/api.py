"""ChainETL REST API.

Production-grade blockchain data API for EVM chains.

    chainetl serve --port 8000
    # Docs at http://localhost:8000/docs
"""

import time
import uuid
from collections.abc import Generator
from contextlib import contextmanager

import structlog
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from chainetl.extractors.evm import EVMExtractor

logger = structlog.get_logger()

# --- App ---

app = FastAPI(
    title="ChainETL API",
    description="Query blockchain data from any EVM chain in real-time.",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# --- Config ---

RPCS: dict[str, str] = {
    "ethereum": "https://eth.llamarpc.com",
    "base": "https://mainnet.base.org",
    "polygon": "https://polygon-rpc.com",
    "arbitrum": "https://arb1.arbitrum.io/rpc",
}


# --- Middleware ---


@app.middleware("http")
async def add_headers(request: Request, call_next) -> Response:
    request_id = str(uuid.uuid4())[:8]
    start = time.monotonic()
    response = await call_next(request)
    elapsed = round((time.monotonic() - start) * 1000, 2)
    response.headers["X-Request-Id"] = request_id
    response.headers["X-Response-Time"] = f"{elapsed}ms"
    response.headers["X-Powered-By"] = "ChainETL"
    return response


# --- Helpers ---


@contextmanager
def get_extractor(chain: str) -> Generator[EVMExtractor, None, None]:
    if chain not in RPCS:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "unsupported_chain",
                "message": f"Chain '{chain}' is not supported",
                "supported": list(RPCS.keys()),
            },
        )
    ext = EVMExtractor(RPCS[chain], chain=chain)
    try:
        yield ext
    finally:
        ext.close()


# --- Models ---


class ErrorResponse(BaseModel):
    error: str
    message: str


class BlockResponse(BaseModel):
    chain: str
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
    value: str = Field(description="Value in wei (string to avoid overflow)")
    gas: int
    gas_price: int | None
    transaction_type: int | None


class TokenTransferResponse(BaseModel):
    transaction_hash: str
    log_index: int
    token_address: str
    token_standard: str
    from_address: str
    to_address: str
    value: str


class BlockDetailResponse(BlockResponse):
    transactions: list[TransactionResponse]


class FullBlockResponse(BlockDetailResponse):
    logs_count: int
    token_transfers: list[TokenTransferResponse]


class ChainResponse(BaseModel):
    chain: str
    latest_block: int
    rpc_url: str


class HealthResponse(BaseModel):
    status: str
    version: str
    chains: int


# --- Routes ---


@app.get("/", response_model=HealthResponse, tags=["System"])
def health() -> HealthResponse:
    """Health check and API info."""
    return HealthResponse(
        status="ok", version="0.2.0", chains=len(RPCS)
    )


@app.get("/chains", response_model=list[ChainResponse], tags=["Chains"])
def list_chains() -> list[ChainResponse]:
    """List all supported chains with their RPC endpoints."""
    results = []
    for name, rpc in RPCS.items():
        with get_extractor(name) as ext:
            try:
                latest = ext.extract_latest_block_number()
            except Exception:
                latest = -1
            results.append(ChainResponse(
                chain=name, latest_block=latest, rpc_url=rpc
            ))
    return results


@app.get(
    "/chains/{chain}",
    response_model=ChainResponse,
    tags=["Chains"],
)
def chain_info(chain: str) -> ChainResponse:
    """Get chain info including latest block number."""
    with get_extractor(chain) as ext:
        latest = ext.extract_latest_block_number()
        return ChainResponse(
            chain=chain, latest_block=latest, rpc_url=RPCS[chain]
        )


@app.get(
    "/chains/{chain}/blocks/latest",
    response_model=BlockResponse,
    tags=["Blocks"],
)
def get_latest_block(chain: str) -> BlockResponse:
    """Get the latest block."""
    with get_extractor(chain) as ext:
        n = ext.extract_latest_block_number()
        block = ext.extract_block(n)
        return BlockResponse(
            chain=chain, number=block.number, hash=block.hash,
            parent_hash=block.parent_hash, timestamp=block.timestamp,
            transaction_count=len(block.transactions),
        )


@app.get(
    "/chains/{chain}/blocks/{block_number}",
    response_model=BlockResponse,
    tags=["Blocks"],
)
def get_block(chain: str, block_number: int) -> BlockResponse:
    """Get a block by number."""
    with get_extractor(chain) as ext:
        try:
            block = ext.extract_block(block_number)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return BlockResponse(
            chain=chain, number=block.number, hash=block.hash,
            parent_hash=block.parent_hash, timestamp=block.timestamp,
            transaction_count=len(block.transactions),
        )


@app.get(
    "/chains/{chain}/blocks/{block_number}/transactions",
    response_model=list[TransactionResponse],
    tags=["Transactions"],
)
def get_block_transactions(
    chain: str, block_number: int
) -> list[TransactionResponse]:
    """Get all transactions in a block."""
    with get_extractor(chain) as ext:
        try:
            _, txs = ext.extract_block_with_transactions(block_number)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return [
            TransactionResponse(
                hash=tx.hash,
                block_number=tx.block_number,
                from_address=tx.from_address,
                to_address=tx.to_address,
                value=str(tx.value),
                gas=tx.gas,
                gas_price=tx.gas_price,
                transaction_type=tx.transaction_type,
            )
            for tx in txs
        ]


@app.get(
    "/chains/{chain}/blocks/{block_number}/full",
    response_model=FullBlockResponse,
    tags=["Blocks"],
)
def get_block_full(chain: str, block_number: int) -> FullBlockResponse:
    """Get a block with all transactions, logs, and token transfers."""
    with get_extractor(chain) as ext:
        try:
            block, txs, logs, transfers = (
                ext.extract_block_with_full_data(block_number)
            )
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return FullBlockResponse(
            chain=chain,
            number=block.number,
            hash=block.hash,
            parent_hash=block.parent_hash,
            timestamp=block.timestamp,
            transaction_count=len(txs),
            transactions=[
                TransactionResponse(
                    hash=tx.hash,
                    block_number=tx.block_number,
                    from_address=tx.from_address,
                    to_address=tx.to_address,
                    value=str(tx.value),
                    gas=tx.gas,
                    gas_price=tx.gas_price,
                    transaction_type=tx.transaction_type,
                )
                for tx in txs
            ],
            logs_count=len(logs),
            token_transfers=[
                TokenTransferResponse(
                    transaction_hash=t.transaction_hash,
                    log_index=t.log_index,
                    token_address=t.token_address,
                    token_standard=t.token_standard,
                    from_address=t.from_address,
                    to_address=t.to_address,
                    value=t.value,
                )
                for t in transfers
            ],
        )
