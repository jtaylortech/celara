"""Base loader interface."""

from abc import ABC, abstractmethod

from chainetl.models.block import Block
from chainetl.models.checkpoint import Checkpoint


class BaseLoader(ABC):
    """Base class for data loaders."""

    @abstractmethod
    def load_block(self, block: Block, chain: str) -> None:
        """Load a block to destination.

        Args:
            block: Block to load
            chain: Chain identifier (e.g., "ethereum", "base")
        """
        pass

    @abstractmethod
    def load_blocks(self, blocks: list[Block], chain: str) -> None:
        """Load multiple blocks to destination.

        Args:
            blocks: List of blocks to load
            chain: Chain identifier (e.g., "ethereum", "base")
        """
        pass

    @abstractmethod
    def save_checkpoint(self, checkpoint: Checkpoint) -> None:
        """Save a checkpoint.

        Args:
            checkpoint: Checkpoint to save
        """
        pass

    @abstractmethod
    def load_checkpoint(self, chain: str) -> Checkpoint | None:
        """Load a checkpoint for a given chain.

        Args:
            chain: Chain identifier (e.g., "ethereum", "base")

        Returns:
            Checkpoint if found, None otherwise
        """
        pass

    @abstractmethod
    def detect_reorg(self, chain: str, new_block: Block) -> bool:
        """Detect if a block indicates a chain reorganization.

        Args:
            chain: Chain identifier (e.g., "ethereum", "base")
            new_block: The new block to check

        Returns:
            True if a reorg is detected, False otherwise
        """
        pass
