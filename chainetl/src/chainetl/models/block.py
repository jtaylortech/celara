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

        Args:
            data: Raw RPC response

        Returns:
            Block instance
        """
        return cls(
            number=int(data["number"], 16),
            hash=data["hash"],
            parent_hash=data["parentHash"],
            timestamp=int(data["timestamp"], 16),
            transactions=data.get("transactions", []),
        )
