"""JSON Lines file loader.

Writes blocks as newline-delimited JSON — no database required.
Each line is a valid JSON object. Compatible with jq, DuckDB, pandas.
"""

import json
from pathlib import Path

import structlog

from chainetl.loaders.base import BaseLoader
from chainetl.models.block import Block
from chainetl.models.checkpoint import Checkpoint

logger = structlog.get_logger()


class JsonLinesLoader(BaseLoader):
    """Write blocks to JSON Lines files."""

    def __init__(self, output_dir: str = "output") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._checkpoint_file = self.output_dir / "checkpoint.json"
        logger.info("jsonl_loader_initialized", output_dir=str(self.output_dir))

    def _blocks_file(self, chain: str) -> Path:
        return self.output_dir / f"{chain}_blocks.jsonl"

    def load_block(self, block: Block, chain: str) -> None:
        with open(self._blocks_file(chain), "a") as f:
            f.write(block.model_dump_json() + "\n")
        logger.info("block_written", chain=chain, block_number=block.number)

    def load_blocks(self, blocks: list[Block], chain: str) -> None:
        if not blocks:
            return
        with open(self._blocks_file(chain), "a") as f:
            for block in blocks:
                f.write(block.model_dump_json() + "\n")
        logger.info("blocks_written", chain=chain, count=len(blocks))

    def save_checkpoint(self, checkpoint: Checkpoint) -> None:
        data = checkpoint.model_dump(mode="json")
        self._checkpoint_file.write_text(json.dumps(data, indent=2))
        logger.info(
            "checkpoint_saved",
            chain=checkpoint.chain,
            block=checkpoint.last_synced_block,
        )

    def load_checkpoint(self, chain: str) -> Checkpoint | None:
        if not self._checkpoint_file.exists():
            return None
        data = json.loads(self._checkpoint_file.read_text())
        if data.get("chain") != chain:
            return None
        return Checkpoint(**data)

    def detect_reorg(self, chain: str, new_block: Block) -> bool:
        """Reorg detection not supported for file output."""
        return False
