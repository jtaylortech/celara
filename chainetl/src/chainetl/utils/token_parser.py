"""Token event parsing utilities.

This module provides utilities for parsing common Ethereum token standards:
- ERC-20: Fungible tokens
- ERC-721: Non-fungible tokens (NFTs)
- ERC-1155: Multi-token standard
"""


import structlog

from chainetl.models.log import Log
from chainetl.models.token_transfer import TokenTransfer

logger = structlog.get_logger()

# ERC-20 Transfer event signature: Transfer(address indexed from, address indexed to, uint256 value)
ERC20_TRANSFER_SIGNATURE = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

# ERC-721 Transfer event signature:
# Transfer(address indexed from, address indexed to, uint256 indexed tokenId)
ERC721_TRANSFER_SIGNATURE = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

# Note: ERC-20 and ERC-721 share the same Transfer signature, but differ in indexed parameters
# ERC-20: 3 topics (signature, from, to) + data (value)
# ERC-721: 4 topics (signature, from, to, tokenId)


def is_erc20_transfer(log: Log) -> bool:
    """Check if a log represents an ERC-20 Transfer event.

    Args:
        log: Log to check

    Returns:
        True if log is an ERC-20 Transfer event
    """
    # ERC-20 Transfer has exactly 3 topics
    return len(log.topics) == 3 and log.topics[0] == ERC20_TRANSFER_SIGNATURE


def is_erc721_transfer(log: Log) -> bool:
    """Check if a log represents an ERC-721 Transfer event.

    Args:
        log: Log to check

    Returns:
        True if log is an ERC-721 Transfer event
    """
    # ERC-721 Transfer has exactly 4 topics (tokenId is indexed)
    return len(log.topics) == 4 and log.topics[0] == ERC721_TRANSFER_SIGNATURE


def parse_token_transfer(
    log: Log, transaction_hash: str, block_number: int
) -> TokenTransfer | None:
    """Parse a log into a TokenTransfer if it's a supported token standard.

    Args:
        log: Log to parse
        transaction_hash: Transaction hash containing this log
        block_number: Block number

    Returns:
        TokenTransfer if log is a supported token transfer, None otherwise
    """
    try:
        # Convert Log to RPC-style dict for processing
        log_dict = {
            "address": log.address,
            "topics": log.topics,
            "data": log.data,
            "logIndex": hex(log.log_index) if log.log_index is not None else "0x0",
            "transactionHash": transaction_hash,
            "blockNumber": hex(block_number),
        }

        # Check for ERC-721 first (4 topics)
        if is_erc721_transfer(log):
            logger.debug(
                "parsing_erc721_transfer",
                token_address=log.address,
                transaction_hash=transaction_hash,
            )
            return TokenTransfer.from_erc721_log(log_dict, transaction_hash, block_number)

        # Check for ERC-20 (3 topics)
        if is_erc20_transfer(log):
            logger.debug(
                "parsing_erc20_transfer",
                token_address=log.address,
                transaction_hash=transaction_hash,
            )
            return TokenTransfer.from_erc20_log(log_dict, transaction_hash, block_number)

        # Not a recognized token transfer
        return None

    except Exception as e:
        logger.warning(
            "failed_to_parse_token_transfer",
            error=str(e),
            log_address=log.address,
            transaction_hash=transaction_hash,
        )
        return None


def parse_token_transfers_from_logs(
    logs: list[Log], transaction_hash: str, block_number: int
) -> list[TokenTransfer]:
    """Parse all token transfers from a list of logs.

    Args:
        logs: List of logs to parse
        transaction_hash: Transaction hash
        block_number: Block number

    Returns:
        List of parsed TokenTransfer objects
    """
    transfers: list[TokenTransfer] = []

    for log in logs:
        transfer = parse_token_transfer(log, transaction_hash, block_number)
        if transfer:
            transfers.append(transfer)

    logger.debug(
        "parsed_token_transfers",
        transaction_hash=transaction_hash,
        total_logs=len(logs),
        token_transfers=len(transfers),
    )

    return transfers
