"""Command-line interface."""

import structlog
import typer

from chainetl.config import settings
from chainetl.extractors.ethereum import EthereumExtractor
from chainetl.loaders.postgres import PostgresLoader

app = typer.Typer(help="ChainETL - Blockchain data pipelines")
logger = structlog.get_logger()


@app.command()
def sync(
    chain: str = typer.Option("ethereum", help="Blockchain to sync"),
    start_block: int | None = typer.Option(None, help="Starting block number"),
    destination: str = typer.Option("postgres", help="Destination (postgres, file)"),
) -> None:
    """Sync blockchain data to destination."""
    logger.info("starting_sync", chain=chain, start_block=start_block, destination=destination)

    if chain != "ethereum":
        typer.echo(f"Chain '{chain}' not supported yet")
        raise typer.Exit(1)

    # Initialize extractor
    extractor = EthereumExtractor(rpc_url=settings.ethereum_rpc_url)

    # Get starting block
    if start_block is None:
        start_block = extractor.extract_latest_block_number()
        typer.echo(f"Starting from latest block: {start_block}")

    # Initialize loader
    if destination == "postgres":
        loader = PostgresLoader(settings.database_url)
    else:
        typer.echo(f"Destination '{destination}' not supported yet")
        raise typer.Exit(1)

    # Extract and load
    try:
        block = extractor.extract_block(start_block)
        loader.load_block(block)
        typer.echo(f"Loaded block {block.number}: {block.hash}")
    except Exception as e:
        logger.exception("sync_failed", error=str(e))
        typer.echo(f"Sync failed: {e}")
        raise typer.Exit(1)


@app.command()
def status() -> None:
    """Show sync status."""
    typer.echo("ChainETL Status:")
    typer.echo("  Chain: ethereum")
    typer.echo("  Status: Ready")
    typer.echo(f"  RPC: {settings.ethereum_rpc_url}")
    typer.echo(f"  Database: {settings.database_url}")


if __name__ == "__main__":
    app()
