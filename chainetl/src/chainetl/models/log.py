from typing import Any

from pydantic import BaseModel, Field


class Log(BaseModel):
    """Ethereum log/event model."""

    address: str = Field(..., description="Contract address")
    topics: list[str] = Field(default_factory=list, description="Indexed topics")
    data: str = Field("0x", description="Data payload")
    log_index: int | None = Field(None, alias="logIndex", description="Log index in block")
    transaction_hash: str | None = Field(None, alias="transactionHash", description="Transaction hash")
    block_number: int | None = Field(None, alias="blockNumber", description="Block number")

    @classmethod
    def from_rpc(cls, data: dict[str, Any]) -> "Log":
        """Create Log model from RPC response."""
        return cls(
            address=data.get("address"),
            topics=data.get("topics", []),
            data=data.get("data", "0x"),
            logIndex=int(data.get("logIndex"), 16) if data.get("logIndex") else None,
            transactionHash=data.get("transactionHash"),
            blockNumber=int(data.get("blockNumber"), 16) if data.get("blockNumber") else None,
        )
