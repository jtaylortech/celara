"""Base extractor interface."""

from abc import ABC, abstractmethod

from chainetl.models.block import Block


class BaseExtractor(ABC):
    """Base class for blockchain extractors.

    All blockchain extractors must implement this interface to ensure
    consistent behavior across different chains (Ethereum, Base, etc.).
    """

    @property
    @abstractmethod
    def chain_name(self) -> str:
        """Get the name of the blockchain.

        Returns:
            Chain name (e.g., "ethereum", "base")
        """
        pass

    @abstractmethod
    def extract_block(self, block_number: int) -> Block:
        """Extract a single block.

        Args:
            block_number: Block number to extract

        Returns:
            Block data

        Raises:
            ValueError: If block not found
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def extract_latest_block_number(self) -> int:
        """Get the latest block number.

        Returns:
            Latest block number

        Raises:
            ValueError: If unable to fetch latest block number
        """
        pass
