"""Command-line interface."""

import signal
from datetime import UTC, datetime

import structlog
import typer

from chainetl.config import settings
from chainetl.extractors.arbitrum import ArbitrumExtractor
from chainetl.extractors.base import BaseExtractor
from chainetl.extractors.base_l2 import BaseL2Extractor
from chainetl.extractors.ethereum import EthereumExtractor
from chainetl.extractors.polygon import PolygonExtractor
from chainetl.loaders.base import BaseLoader
from chainetl.loaders.postgres import PostgresLoader
from chainetl.models.checkpoint import Checkpoint

app = typer.Typer(help="ChainETL - Blockchain data pipelines")
logger = structlog.get_logger()

_shutdown_requested = False

# Chain → (ExtractorClass, RPC URL setting)
SUPPORTED_CHAINS: dict[str, tuple[type[BaseExtractor], str]] = {
    "ethereum": (EthereumExtractor, str(settings.ethereum_rpc_url)),
    "base": (BaseL2Extractor, str(settings.base_rpc_url)),
    "polygon": (PolygonExtractor, str(settings.polygon_rpc_url)),
    "arbitrum": (ArbitrumExtractor, str(settings.arbitrum_rpc_url)),
}


def _signal_handler(signum: int, frame: object) -> None:
    global _shutdown_requested
    signal_name = signal.Signals(signum).name
    logger.info("shutdown_signal_received", signal=signal_name)
    typer.echo(
        f"\n⚠️  Shutdown signal ({signal_name}). Finishing current block...",
        err=True,
    )
    _shutdown_requested = True


signal.signal(signal.SIGTERM, _signal_handler)
signal.signal(signal.SIGINT, _signal_handler)


def _get_extractor(chain: str) -> BaseExtractor:
    """Create extractor for the given chain."""
    if chain not in SUPPORTED_CHAINS:
        chain_list = ", ".join(SUPPORTED_CHAINS)
        typer.echo(
            f"❌ Unsupported chain: '{chain}'. Supported: {chain_list}",
            err=True,
        )
        raise typer.Exit(1)
    cls, rpc_url = SUPPORTED_CHAINS[chain]
    return cls(rpc_url=rpc_url)


@app.command()
def sync(
    chain: str = typer.Option("ethereum", help="Blockchain to sync"),
    start_block: int | None = typer.Option(None, help="Starting block number"),
    destination: str = typer.Option("postgres", help="Destination"),
    resume: bool = typer.Option(False, help="Resume from last checkpoint"),
    count: int = typer.Option(1, help="Number of blocks to sync"),
) -> None:
    """Sync blockchain data to destination."""
    logger.info(
        "starting_sync",
        chain=chain,
        start_block=start_block,
        destination=destination,
        resume=resume,
        count=count,
    )

    extractor = _get_extractor(chain)

    # Initialize loader
    if destination == "postgres":
        loader: BaseLoader = PostgresLoader(settings.database_url)
    elif destination == "jsonl":
        from chainetl.loaders.jsonl import JsonLinesLoader
        loader = JsonLinesLoader()
    else:
        typer.echo(
            f"❌ Unsupported destination: '{destination}'. "
            f"Supported: postgres, jsonl",
            err=True,
        )
        raise typer.Exit(1)

    # Resolve start block
    if resume:
        checkpoint = loader.load_checkpoint(chain)
        if checkpoint:
            start_block = checkpoint.last_synced_block + 1
            typer.echo(
                f"Resuming from checkpoint: block "
                f"{checkpoint.last_synced_block} -> {start_block}"
            )
        else:
            typer.echo("No checkpoint found, starting from latest block")
            start_block = extractor.extract_latest_block_number()
    elif start_block is None:
        start_block = extractor.extract_latest_block_number()
        typer.echo(f"Starting from latest block: {start_block}")
    else:
        typer.echo(f"Starting from block: {start_block}")

    try:
        try:
            if count == 1:
                block = extractor.extract_block(start_block)
                if loader.detect_reorg(chain, block):
                    typer.echo(
                        f"WARNING: Reorg detected at block {block.number}",
                        err=True,
                    )
                loader.load_block(block, chain)
                typer.echo(f"Loaded block {block.number}: {block.hash}")
            else:
                end_block = start_block + count - 1
                typer.echo(
                    f"Syncing blocks {start_block} to {end_block} "
                    f"({count} blocks)"
                )

                if count >= 10:
                    with typer.progressbar(
                        range(start_block, end_block + 1),
                        label="Extracting blocks",
                        show_pos=True,
                    ) as progress:
                        blocks = []
                        for block_num in progress:
                            blocks.append(
                                extractor.extract_block(block_num)
                            )
                else:
                    blocks = extractor.extract_blocks(start_block, end_block)

                if blocks and loader.detect_reorg(chain, blocks[0]):
                    typer.echo(
                        f"WARNING: Reorg detected at block "
                        f"{blocks[0].number}",
                        err=True,
                    )

                loader.load_blocks(blocks, chain)
                typer.echo(f"Loaded {len(blocks)} blocks")
                block = blocks[-1]

            # Save checkpoint
            checkpoint = Checkpoint(
                chain=chain,
                last_synced_block=block.number,
                last_synced_hash=block.hash,
                synced_at=datetime.now(UTC),
                status="active",
            )
            loader.save_checkpoint(checkpoint)
            typer.echo(f"Checkpoint saved at block {block.number}")
        finally:
            extractor.close()

    except Exception as e:
        logger.exception("sync_failed", error=str(e))
        typer.echo(f"\n❌ Sync failed: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def status(
    chain: str = typer.Option("ethereum", help="Blockchain to check"),
) -> None:
    """Show sync status and checkpoint information."""
    if chain not in SUPPORTED_CHAINS:
        chain_list = ", ".join(SUPPORTED_CHAINS)
        typer.echo(
            f"❌ Unsupported chain: '{chain}'. Supported: {chain_list}",
            err=True,
        )
        raise typer.Exit(1)

    _, rpc_url = SUPPORTED_CHAINS[chain]
    typer.echo("ChainETL Status:")
    typer.echo(f"  Chain: {chain}")
    typer.echo("  Status: Ready")
    typer.echo(f"  RPC: {rpc_url}")
    typer.echo(f"  Database: {settings.database_url}")

    try:
        loader = PostgresLoader(settings.database_url)
        checkpoint = loader.load_checkpoint(chain)
        if checkpoint:
            typer.echo("\nCheckpoint:")
            typer.echo(f"  Last synced block: {checkpoint.last_synced_block}")
            typer.echo(f"  Last synced hash: {checkpoint.last_synced_hash}")
            typer.echo(f"  Synced at: {checkpoint.synced_at}")
            typer.echo(f"  Status: {checkpoint.status}")
        else:
            typer.echo(f"\nCheckpoint: None (no {chain} sync yet)")
    except Exception as e:
        logger.warning("failed_to_load_checkpoint", error=str(e), chain=chain)


@app.command()
def chains() -> None:
    """List supported blockchains."""
    typer.echo("Supported chains:")
    for name, (_, rpc_url) in SUPPORTED_CHAINS.items():
        typer.echo(f"  • {name:12s} {rpc_url}")


if __name__ == "__main__":
    app()
