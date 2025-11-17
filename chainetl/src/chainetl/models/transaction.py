from typing import Any

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    """Ethereum transaction model."""

    hash: str = Field(..., description="Transaction hash")
    from_address: str = Field(..., alias="from", description="Sender address")
    to_address: str | None = Field(None, alias="to", description="Recipient address")
    value: int = Field(..., description="Value in wei")
    gas: int = Field(..., description="Gas limit")
    gas_price: int | None = Field(None, alias="gasPrice", description="Gas price in wei")
    nonce: int = Field(..., description="Transaction nonce")
    input: str = Field("0x", description="Input/data")

    @classmethod
    def from_rpc(cls, data: dict[str, Any]) -> "Transaction":
        """Create Transaction from RPC response dict."""
        return cls(
            hash=data["hash"],
            **{
                "from": data.get("from"),
                "to": data.get("to"),
                "value": int(data.get("value", "0x0"), 16),
                "gas": int(data.get("gas", "0x0"), 16),
                "gasPrice": int(data.get("gasPrice", "0x0"), 16) if data.get("gasPrice") else None,
                "nonce": int(data.get("nonce", "0x0"), 16),
                "input": data.get("input", "0x"),
            },
        )
