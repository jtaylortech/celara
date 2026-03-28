# API Reference

ChainETL includes a self-hosted FastAPI server for querying blockchain data over HTTP.

## Start the Server

```bash
chainetl serve --port 8000
# or
uvicorn chainetl.api:app --host 0.0.0.0 --port 8000
```

Interactive docs at `http://localhost:8000/docs` (Swagger) and `/redoc` (ReDoc).

## Endpoints

### `GET /`
Health check. Returns API version and supported chain count.

### `GET /chains`
List all supported chains with latest block numbers.

### `GET /chains/{chain}`
Chain info for a specific chain.

### `GET /chains/{chain}/blocks/latest`
Most recent block on the chain.

### `GET /chains/{chain}/blocks/{block_number}`
Specific block by number. Returns hash, parent hash, timestamp, transaction count.

### `GET /chains/{chain}/blocks/{block_number}/transactions`
All transactions in a block. Returns hash, from, to, value (wei as string), gas, type.

### `GET /chains/{chain}/blocks/{block_number}/full`
Block with all transactions, log count, and parsed token transfers. Most comprehensive endpoint.

## Response Headers

| Header | Description |
|--------|-------------|
| `X-Request-Id` | Unique request identifier (8 chars) |
| `X-Response-Time` | Server processing time in ms |
| `X-Powered-By` | `ChainETL` |

## Errors

```json
// 400 — unsupported chain
{"error": "unsupported_chain", "message": "Chain 'solana' is not supported", "supported": ["ethereum", "base", "polygon", "arbitrum"]}

// 404 — block not found
{"detail": "Block 999999999999 not found on ethereum"}
```

## CORS

Enabled for all origins (`*`). GET requests only.
