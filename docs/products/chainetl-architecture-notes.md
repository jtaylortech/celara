# ChainETL — Architecture notes (brief)

This short note documents the core dataflow, responsibilities of components, and key edge-cases to consider while developing ChainETL.

## Core components

- Extractors: connect to RPC endpoints and produce normalized records (blocks, transactions, events).
- Loaders: persist records to destinations (Postgres, files). Must be idempotent and handle upserts.
- Models: Pydantic models provide validation and serialization helpers.
- CLI: user-facing commands (sync, backfill, status) that orchestrate extractors and loaders.
- RPC client: thin JSON-RPC wrapper with basic error handling and a synchronous HTTP client.

## Data flow (single-block sync)

1. CLI parses args and selects chain, start block, and destination.
2. CLI initializes the appropriate Extractor (e.g. `EthereumExtractor`).
3. Extractor uses `RPCClient.call("eth_getBlockByNumber", ...)` to fetch block data.
4. Extractor converts RPC JSON into a `Block` model (`Block.from_rpc`).
5. Loader receives the `Block` model and writes to the destination (Postgres, file).
6. CLI reports success / failure.

## Edge cases and recommended handling

- Reorgs (chain reorganizations):
  - Detect by comparing parent hashes when loading sequential blocks.
  - Keep a configurable checkpoint depth (e.g. 6 blocks) before marking data as finalized.
  - Implement rollback or compensating writes for replaced blocks.

- Idempotency:
  - Use natural keys (block number) and upserts (merge) to avoid duplicate rows.
  - Track sync checkpoints separately so restarts can resume safely.

- Retry and backoff:
  - For transient RPC/network errors, retry with exponential backoff.
  - Limit retries and escalate persistent failures to alerts.

- Batching and performance:
  - Batch writes in loaders for higher throughput.
  - Use connection pooling on DB clients and tune transaction sizes.

- Observability:
  - Emit structured logs (already using structlog) including chain, block_number, and duration.
  - Record metrics for RPC latency, blocks processed, and error rates.

## Next improvements (low-risk)

- Add checkpoint storage (simple table in Postgres) and a `resume` mode in the CLI.
- Add reorg detection and a safe-apply window before marking blocks finalized.
- Convert `RPCClient` to async with `httpx.AsyncClient` for higher concurrency (carefully).

---

This document is intentionally short — I can expand any section into a design doc or PR if you'd like.
