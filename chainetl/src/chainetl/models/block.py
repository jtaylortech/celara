"""Block data models."""

from typing import Any

from pydantic import BaseModel, Field


class Block(BaseModel):
    """Blockchain block."""

    number: int = Field(..., description="Block number")
    hash: str = Field(..., description="Block hash")
    parent_hash: str = Field(..., description="Parent block hash")
    timestamp: int = Field(..., description="Block timestamp (Unix)")
    transactions: list[str] = Field(default_factory=list, description="Transaction hashes")

    @classmethod
    def from_rpc(cls, data: dict[str, Any]) -> "Block":
        """Parse RPC response into Block model.

        Handles both tx hash lists (full_txs=False) and
        full tx objects (full_txs=True) by extracting hashes.
        """
        raw_txs = data.get("transactions", [])
        tx_hashes = [
            t["hash"] if isinstance(t, dict) else t for t in raw_txs
        ]
        return cls(
            number=int(data["number"], 16),
            hash=data["hash"],
            parent_hash=data["parentHash"],
            timestamp=int(data["timestamp"], 16),
            transactions=tx_hashes,
        )
