"""Transaction data models."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Transaction(BaseModel):
    """Ethereum transaction model.

    Represents a complete transaction with all relevant data for analysis.
    Supports both legacy and EIP-1559 transactions.
    """

    # Core transaction identifiers
    hash: str = Field(..., description="Transaction hash")
    block_number: int = Field(..., description="Block number")
    block_hash: str = Field(..., description="Block hash")
    transaction_index: int = Field(..., description="Transaction index in block")

    # Sender and recipient
    from_address: str = Field(..., alias="from", description="Sender address")
    to_address: str | None = Field(
        None, alias="to", description="Recipient address (None for contract creation)"
    )

    # Value and data
    value: int = Field(..., description="Value transferred in wei")
    input: str = Field("0x", description="Transaction input data")

    # Gas parameters (legacy)
    gas: int = Field(..., description="Gas limit")
    gas_price: int | None = Field(
        None, alias="gasPrice", description="Gas price in wei (legacy transactions)"
    )

    # Gas parameters (EIP-1559)
    max_fee_per_gas: int | None = Field(
        None, alias="maxFeePerGas", description="Max fee per gas (EIP-1559)"
    )
    max_priority_fee_per_gas: int | None = Field(
        None, alias="maxPriorityFeePerGas", description="Max priority fee per gas (EIP-1559)"
    )

    # Transaction metadata
    nonce: int = Field(..., description="Transaction nonce")
    transaction_type: int | None = Field(
        None, alias="type", description="Transaction type (0=legacy, 2=EIP-1559)"
    )

    # Chain-specific
    chain_id: int | None = Field(None, alias="chainId", description="Chain ID")

    # Signature (v, r, s)
    v: str | None = Field(None, description="ECDSA recovery id")
    r: str | None = Field(None, description="ECDSA signature r")
    s: str | None = Field(None, description="ECDSA signature s")

    model_config = ConfigDict(populate_by_name=True)  # Allow both alias and field name

    @classmethod
    def from_rpc(cls, data: dict[str, Any]) -> "Transaction":
        """Create Transaction from RPC response.

        Args:
            data: Raw RPC transaction data

        Returns:
            Transaction instance

        Raises:
            ValueError: If required fields are missing
        """
        return cls(
            hash=data["hash"],
            block_number=int(data["blockNumber"], 16),
            block_hash=data["blockHash"],
            transaction_index=int(data["transactionIndex"], 16),
            **{
                "from": data.get("from"),
                "to": data.get("to"),
                "value": int(data.get("value", "0x0"), 16),
                "input": data.get("input", "0x"),
                "gas": int(data.get("gas", "0x0"), 16),
                "gasPrice": int(data.get("gasPrice", "0x0"), 16) if data.get("gasPrice") else None,
                "maxFeePerGas": int(data.get("maxFeePerGas", "0x0"), 16)
                if data.get("maxFeePerGas")
                else None,
                "maxPriorityFeePerGas": (
                    int(data.get("maxPriorityFeePerGas", "0x0"), 16)
                    if data.get("maxPriorityFeePerGas")
                    else None
                ),
                "nonce": int(data.get("nonce", "0x0"), 16),
                "type": int(data.get("type", "0x0"), 16) if data.get("type") else None,
                "chainId": int(data.get("chainId", "0x0"), 16) if data.get("chainId") else None,
                "v": data.get("v"),
                "r": data.get("r"),
                "s": data.get("s"),
            },
        )
