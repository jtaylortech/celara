# Data Models

All models use Pydantic v2 with `from_rpc()` classmethods that handle hex→int conversion.

## Block

```python
class Block(BaseModel):
    number: int          # Block height
    hash: str            # 0x-prefixed, 66 chars
    parent_hash: str     # Previous block hash
    timestamp: int       # Unix timestamp
    transactions: list[str]  # Transaction hashes (or full objects)
```

`Block.from_rpc(data)` handles both `eth_getBlockByNumber(n, false)` (tx hashes) and `eth_getBlockByNumber(n, true)` (full tx objects) — it extracts hashes from dicts automatically.

## Transaction

```python
class Transaction(BaseModel):
    hash: str
    block_number: int
    block_hash: str
    transaction_index: int
    from_address: str        # Sender
    to_address: str | None   # Recipient (None = contract creation)
    value: int               # Wei
    input: str               # Calldata
    gas: int                 # Gas limit
    gas_price: int | None    # Legacy transactions
    max_fee_per_gas: int | None          # EIP-1559
    max_priority_fee_per_gas: int | None # EIP-1559
    nonce: int
    transaction_type: int | None  # 0=legacy, 2=EIP-1559
    chain_id: int | None
    v: str | None            # ECDSA signature
    r: str | None
    s: str | None
```

## Log

```python
class Log(BaseModel):
    address: str             # Contract that emitted the event
    topics: list[str]        # Indexed parameters (topic[0] = event signature)
    data: str                # Non-indexed parameters (ABI-encoded)
    log_index: int | None
    transaction_hash: str | None
    block_number: int | None
    block_hash: str | None
```

## TokenTransfer

Parsed from Transfer event logs. Supports ERC-20 (fungible) and ERC-721 (NFT).

```python
class TokenTransfer(BaseModel):
    transaction_hash: str
    log_index: int
    block_number: int
    token_address: str       # Token contract
    token_standard: str      # "ERC-20" or "ERC-721"
    from_address: str
    to_address: str
    value: str               # Amount (ERC-20) or token ID (ERC-721)
```

**How detection works**: ERC-20 and ERC-721 share the same Transfer event signature. They're distinguished by topic count:
- 3 topics = ERC-20 (value in `data`)
- 4 topics = ERC-721 (tokenId is indexed as topic[3])

## Checkpoint

```python
class Checkpoint(BaseModel):
    chain: str               # "ethereum", "polygon", etc.
    last_synced_block: int
    last_synced_hash: str
    synced_at: datetime
    status: str              # "active", "paused", "error"
```
