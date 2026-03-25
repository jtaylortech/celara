"""Command-line interface."""

import signal
from datetime import UTC, datetime

import structlog
import typer

from chainetl.config import settings
from chainetl.extractors.base import BaseExtractor
from chainetl.extractors.base_l2 import BaseL2Extractor
from chainetl.extractors.ethereum import EthereumExtractor
from chainetl.loaders.postgres import PostgresLoader
from chainetl.models.checkpoint import Checkpoint

app = typer.Typer(help="ChainETL - Blockchain data pipelines")
logger = structlog.get_logger()

# Global flag for graceful shutdown
_shutdown_requested = False


def _signal_handler(signum: int, frame: object) -> None:
    """Handle shutdown signals gracefully."""
    global _shutdown_requested
    signal_name = signal.Signals(signum).name
    logger.info("shutdown_signal_received", signal=signal_name)
    typer.echo(
        f"\n⚠️  Shutdown signal received ({signal_name}). Finishing current block...", err=True
    )
    _shutdown_requested = True


# Register signal handlers for graceful shutdown
signal.signal(signal.SIGTERM, _signal_handler)
signal.signal(signal.SIGINT, _signal_handler)


@app.command()
def sync(
    chain: str = typer.Option("ethereum", help="Blockchain to sync (ethereum, base)"),
    start_block: int | None = typer.Option(None, help="Starting block number"),
    destination: str = typer.Option("postgres", help="Destination (postgres, file)"),
    resume: bool = typer.Option(False, help="Resume from last checkpoint"),
    count: int = typer.Option(1, help="Number of blocks to sync"),
) -> None:
    """Sync blockchain data to destination.

    This command extracts blocks from the configured RPC endpoint and writes
    them to the configured destination. The optional `start_block` sets the
    block number to extract; if omitted the extractor's latest block number
    will be used.

    Use --resume to continue from the last checkpoint. If a checkpoint exists,
    it will start from the next block after the checkpoint.

    Use --count to specify how many blocks to sync (default: 1).

    Examples:
        Sync 10 Ethereum blocks starting from block 18000000:
        $ chainetl sync --chain ethereum --start-block 18000000 --count 10

        Sync 100 Base L2 blocks starting from block 10000000:
        $ chainetl sync --chain base --start-block 10000000 --count 100

        Resume Ethereum sync from last checkpoint:
        $ chainetl sync --chain ethereum --resume --count 1000

        Resume Base L2 sync from last checkpoint:
        $ chainetl sync --chain base --resume --count 1000
    """

    # Log the incoming request; start_block may be resolved later.
    logger.info(
        "starting_sync",
        chain=chain,
        start_block=start_block,
        destination=destination,
        resume=resume,
        count=count,
    )

    # Initialize extractor based on chain
    extractor: BaseExtractor
    if chain == "ethereum":
        extractor = EthereumExtractor(rpc_url=str(settings.ethereum_rpc_url))
    elif chain == "base":
        extractor = BaseL2Extractor(rpc_url=str(settings.base_rpc_url))
    else:
        typer.echo(f"❌ Error: Chain '{chain}' is not supported.", err=True)
        typer.echo("", err=True)
        typer.echo("Supported chains:", err=True)
        typer.echo("  • ethereum - Ethereum mainnet", err=True)
        typer.echo("  • base     - Base L2", err=True)
        typer.echo("", err=True)
        typer.echo("Example:", err=True)
        typer.echo("  chainetl sync --chain ethereum --start-block 18000000", err=True)
        raise typer.Exit(1)

    # Initialize loader
    if destination == "postgres":
        loader = PostgresLoader(settings.database_url)
    else:
        typer.echo(f"❌ Error: Destination '{destination}' is not supported.", err=True)
        typer.echo("", err=True)
        typer.echo("Supported destinations:", err=True)
        typer.echo("  • postgres - PostgreSQL database", err=True)
        typer.echo("", err=True)
        typer.echo("Configure your database in .env:", err=True)
        typer.echo("  DATABASE_URL=postgresql://user:password@localhost/chainetl_dev", err=True)
        raise typer.Exit(1)

    # Get starting block
    if resume:
        checkpoint = loader.load_checkpoint(chain)
        if checkpoint:
            start_block = checkpoint.last_synced_block + 1
            typer.echo(
                f"Resuming from checkpoint: block {checkpoint.last_synced_block} -> {start_block}"
            )
        else:
            typer.echo("No checkpoint found, starting from latest block")
            start_block = extractor.extract_latest_block_number()
    elif start_block is None:
        start_block = extractor.extract_latest_block_number()
        typer.echo(f"Starting from latest block: {start_block}")
    else:
        typer.echo(f"Starting from block: {start_block}")

    # Extract and load
    try:
        try:
            if count == 1:
                # Single block extraction
                block = extractor.extract_block(start_block)

                # Check for reorg
                if loader.detect_reorg(chain, block):
                    typer.echo(
                        f"WARNING: Chain reorganization detected at block {block.number}",
                        err=True,
                    )
                    typer.echo(
                        "The new block's parent hash doesn't match the previous block.",
                        err=True,
                    )
                    typer.echo("Continuing with sync (reorg handling is basic).", err=True)

                loader.load_block(block, chain)
                typer.echo(f"Loaded block {block.number}: {block.hash}")

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

            else:
                # Batch extraction
                end_block = start_block + count - 1
                typer.echo(f"Syncing blocks {start_block} to {end_block} ({count} blocks)")

                # Show progress for larger batches
                if count >= 10:
                    with typer.progressbar(
                        range(start_block, end_block + 1),
                        label="Extracting blocks",
                        show_pos=True,
                    ) as progress:
                        blocks = []
                        for block_num in progress:
                            block = extractor.extract_block(block_num)
                            blocks.append(block)
                else:
                    blocks = extractor.extract_blocks(start_block, end_block)

                # Check for reorg in first block
                if blocks and loader.detect_reorg(chain, blocks[0]):
                    typer.echo(
                        f"WARNING: Chain reorganization detected at block {blocks[0].number}",
                        err=True,
                    )
                    typer.echo(
                        "The new block's parent hash doesn't match the previous block.",
                        err=True,
                    )
                    typer.echo("Continuing with sync (reorg handling is basic).", err=True)

                loader.load_blocks(blocks, chain)
                typer.echo(f"Loaded {len(blocks)} blocks")

                # Save checkpoint at the last block
                last_block = blocks[-1]
                checkpoint = Checkpoint(
                    chain=chain,
                    last_synced_block=last_block.number,
                    last_synced_hash=last_block.hash,
                    synced_at=datetime.now(UTC),
                    status="active",
                )
                loader.save_checkpoint(checkpoint)
                typer.echo(f"Checkpoint saved at block {last_block.number}")
        finally:
            # Always cleanup RPC client
            extractor.close()

    except Exception as e:
        logger.exception("sync_failed", error=str(e))
        typer.echo(f"\n❌ Sync failed: {e}", err=True)
        typer.echo("", err=True)
        typer.echo("Common issues:", err=True)
        typer.echo("  • RPC endpoint unreachable - Check your network connection", err=True)
        typer.echo("  • Database connection failed - Verify DATABASE_URL in .env", err=True)
        typer.echo("  • Block not found - Try a different block number", err=True)
        typer.echo("", err=True)
        typer.echo("Check logs above for detailed error information.", err=True)
        raise typer.Exit(1)


@app.command()
def status(
    chain: str = typer.Option("ethereum", help="Blockchain to check (ethereum, base)"),
) -> None:
    """Show sync status and checkpoint information.

    Examples:
        Check Ethereum sync status:
        $ chainetl status --chain ethereum

        Check Base L2 sync status:
        $ chainetl status --chain base
    """
    typer.echo("ChainETL Status:")
    typer.echo(f"  Chain: {chain}")
    typer.echo("  Status: Ready")

    # Show RPC endpoint for the chain
    if chain == "ethereum":
        typer.echo(f"  RPC: {str(settings.ethereum_rpc_url)}")
    elif chain == "base":
        typer.echo(f"  RPC: {str(settings.base_rpc_url)}")
    else:
        typer.echo(f"❌ Error: Chain '{chain}' is not supported.", err=True)
        typer.echo("Supported chains: ethereum, base", err=True)
        raise typer.Exit(1)

    typer.echo(f"  Database: {settings.database_url}")

    # Show checkpoint if available
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


if __name__ == "__main__":
    app()
