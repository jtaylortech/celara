"""Token transfer data models."""

from typing import Any

from pydantic import BaseModel, Field


class TokenTransfer(BaseModel):
    """Token transfer event (ERC-20, ERC-721, ERC-1155).

    Represents a parsed token transfer event from a smart contract log.
    Supports multiple token standards:
    - ERC-20: Fungible tokens
    - ERC-721: Non-fungible tokens (NFTs)
    - ERC-1155: Multi-token standard
    """

    # Core transfer data
    transaction_hash: str = Field(..., description="Transaction hash containing this transfer")
    log_index: int = Field(..., description="Log index in the transaction")
    block_number: int = Field(..., description="Block number")

    # Token contract information
    token_address: str = Field(..., description="Token contract address")
    token_standard: str = Field(..., description="Token standard (ERC-20, ERC-721, ERC-1155)")

    # Transfer participants
    from_address: str = Field(..., description="Sender address (from)")
    to_address: str = Field(..., description="Recipient address (to)")

    # Transfer amount/id
    value: str = Field(..., description="Amount transferred (for ERC-20) or token ID (for ERC-721)")

    # Optional metadata
    token_name: str | None = Field(None, description="Token name (if known)")
    token_symbol: str | None = Field(None, description="Token symbol (if known)")
    token_decimals: int | None = Field(None, description="Token decimals (for ERC-20)")

    @classmethod
    def from_erc20_log(
        cls,
        log_data: dict[str, Any],
        transaction_hash: str,
        block_number: int,
    ) -> "TokenTransfer":
        """Create TokenTransfer from ERC-20 Transfer event.

        ERC-20 Transfer event signature:
        Transfer(address indexed from, address indexed to, uint256 value)

        Args:
            log_data: Raw log data from RPC
            transaction_hash: Transaction hash
            block_number: Block number

        Returns:
            TokenTransfer instance

        Raises:
            ValueError: If log data is invalid or doesn't match ERC-20 format
        """
        topics = log_data.get("topics", [])
        if len(topics) < 3:
            raise ValueError("Invalid ERC-20 Transfer event: not enough topics")

        # Topics: [event_signature, from_address, to_address]
        # Data: value (uint256)
        from_address = "0x" + topics[1][-40:]  # Last 40 chars (20 bytes)
        to_address = "0x" + topics[2][-40:]

        # Parse value from data field
        data_hex = log_data.get("data", "0x0")
        value = str(int(data_hex, 16))  # Convert hex to decimal string

        return cls(
            transaction_hash=transaction_hash,
            log_index=int(log_data.get("logIndex", "0x0"), 16),
            block_number=block_number,
            token_address=log_data.get("address", ""),
            token_standard="ERC-20",
            from_address=from_address,
            to_address=to_address,
            value=value,
        )

    @classmethod
    def from_erc721_log(
        cls,
        log_data: dict[str, Any],
        transaction_hash: str,
        block_number: int,
    ) -> "TokenTransfer":
        """Create TokenTransfer from ERC-721 Transfer event.

        ERC-721 Transfer event signature:
        Transfer(address indexed from, address indexed to, uint256 indexed tokenId)

        Args:
            log_data: Raw log data from RPC
            transaction_hash: Transaction hash
            block_number: Block number

        Returns:
            TokenTransfer instance

        Raises:
            ValueError: If log data is invalid or doesn't match ERC-721 format
        """
        topics = log_data.get("topics", [])
        if len(topics) < 4:
            raise ValueError("Invalid ERC-721 Transfer event: not enough topics")

        # Topics: [event_signature, from_address, to_address, token_id]
        from_address = "0x" + topics[1][-40:]
        to_address = "0x" + topics[2][-40:]
        token_id = str(int(topics[3], 16))  # Token ID as decimal string

        return cls(
            transaction_hash=transaction_hash,
            log_index=int(log_data.get("logIndex", "0x0"), 16),
            block_number=block_number,
            token_address=log_data.get("address", ""),
            token_standard="ERC-721",
            from_address=from_address,
            to_address=to_address,
            value=token_id,  # For NFTs, value is the token ID
        )
