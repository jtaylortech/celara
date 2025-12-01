"""Ethereum blockchain extractor."""

import structlog

from chainetl.extractors.base import BaseExtractor
from chainetl.models.block import Block
from chainetl.utils.rpc import RPCClient

logger = structlog.get_logger()


class EthereumExtractor(BaseExtractor):
    """Extract data from Ethereum blockchain."""

    def __init__(self, rpc_url: str) -> None:
        """Initialize Ethereum extractor.

        Args:
            rpc_url: Ethereum RPC endpoint URL
        """
        self.rpc = RPCClient(str(rpc_url))
        logger.info("ethereum_extractor_initialized", rpc_url=str(rpc_url))

    @property
    def chain_name(self) -> str:
        """Get the name of the blockchain.

        Returns:
            "ethereum"
        """
        return "ethereum"

    def extract_block(self, block_number: int) -> Block:
        """Extract a single block.

        Args:
            block_number: Block number to extract

        Returns:
            Block data

        Raises:
            ValueError: If block not found
        """
        logger.info("extracting_block", block_number=block_number)

        data = self.rpc.call("eth_getBlockByNumber", [hex(block_number), False])

        if data is None:
            raise ValueError(f"Block {block_number} not found")

        return Block.from_rpc(data)

    def extract_blocks(self, start_block: int, end_block: int) -> list[Block]:
        """Extract a range of blocks.

        Args:
            start_block: Starting block number (inclusive)
            end_block: Ending block number (inclusive)

        Returns:
            List of blocks

        Raises:
            ValueError: If start_block > end_block or if any block not found
        """
        if start_block > end_block:
            raise ValueError(f"start_block ({start_block}) must be <= end_block ({end_block})")

        logger.info("extracting_blocks", start_block=start_block, end_block=end_block)

        blocks = []
        for block_number in range(start_block, end_block + 1):
            block = self.extract_block(block_number)
            blocks.append(block)

        logger.info("blocks_extracted", count=len(blocks))
        return blocks

    def extract_latest_block_number(self) -> int:
        """Get the latest block number.

        Returns:
            Latest block number
        """
        result = self.rpc.call("eth_blockNumber", [])
        return int(result, 16)

    def close(self) -> None:
        """Close the RPC client connection."""
        self.rpc.close()
        logger.info("ethereum_extractor_closed")
