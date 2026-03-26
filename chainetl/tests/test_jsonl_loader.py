"""Tests for JSON Lines loader."""

import json

from chainetl.loaders.jsonl import JsonLinesLoader
from chainetl.models.block import Block
from chainetl.models.checkpoint import Checkpoint


def test_load_block(tmp_path) -> None:
    loader = JsonLinesLoader(str(tmp_path))
    block = Block(
        number=100,
        hash="0x" + "a" * 64,
        parent_hash="0x" + "b" * 64,
        timestamp=1234567890,
    )
    loader.load_block(block, "ethereum")

    lines = (tmp_path / "ethereum_blocks.jsonl").read_text().strip().split("\n")
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["number"] == 100


def test_load_blocks_batch(tmp_path) -> None:
    loader = JsonLinesLoader(str(tmp_path))
    blocks = [
        Block(number=i, hash=f"0x{i:064x}", parent_hash=f"0x{i-1:064x}", timestamp=1000 + i)
        for i in range(1, 6)
    ]
    loader.load_blocks(blocks, "ethereum")

    lines = (tmp_path / "ethereum_blocks.jsonl").read_text().strip().split("\n")
    assert len(lines) == 5


def test_load_blocks_empty(tmp_path) -> None:
    loader = JsonLinesLoader(str(tmp_path))
    loader.load_blocks([], "ethereum")
    assert not (tmp_path / "ethereum_blocks.jsonl").exists()


def test_checkpoint_roundtrip(tmp_path) -> None:
    loader = JsonLinesLoader(str(tmp_path))
    cp = Checkpoint(chain="ethereum", last_synced_block=100, last_synced_hash="0x" + "a" * 64)
    loader.save_checkpoint(cp)

    loaded = loader.load_checkpoint("ethereum")
    assert loaded is not None
    assert loaded.last_synced_block == 100


def test_checkpoint_wrong_chain(tmp_path) -> None:
    loader = JsonLinesLoader(str(tmp_path))
    cp = Checkpoint(chain="ethereum", last_synced_block=100, last_synced_hash="0x" + "a" * 64)
    loader.save_checkpoint(cp)

    assert loader.load_checkpoint("polygon") is None


def test_checkpoint_missing(tmp_path) -> None:
    loader = JsonLinesLoader(str(tmp_path))
    assert loader.load_checkpoint("ethereum") is None


def test_detect_reorg_always_false(tmp_path) -> None:
    loader = JsonLinesLoader(str(tmp_path))
    block = Block(number=100, hash="0x" + "a" * 64, parent_hash="0x" + "b" * 64, timestamp=1000)
    assert loader.detect_reorg("ethereum", block) is False
