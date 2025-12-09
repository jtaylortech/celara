"""Command-line interface."""

import time

import typer
from prometheus_client import start_http_server

from chainwatch.config import settings
from chainwatch.exporters.ethereum import EthereumExporter

app = typer.Typer(help="ChainWatch - Observability for decentralized systems")


@app.command()
def exporter(
    chain: str = typer.Option("ethereum", help="Chain to export metrics for"),
    port: int = typer.Option(settings.exporter_port, help="Prometheus metrics port"),
    interval: int = typer.Option(settings.scrape_interval, help="Scrape interval in seconds"),
) -> None:
    """Run Prometheus metrics exporter.

    Exposes blockchain node metrics at http://localhost:{port}/metrics

    Examples:
        chainwatch exporter --chain ethereum --port 9100
        chainwatch exporter --chain ethereum --interval 30
    """
    if chain == "ethereum":
        exporter_instance = EthereumExporter(settings.ethereum_rpc_url)
        typer.echo(f"Starting Ethereum exporter on port {port}")
        typer.echo(f"RPC: {settings.ethereum_rpc_url}")
    else:
        typer.echo(f"Chain '{chain}' not supported yet. Supported: ethereum")
        raise typer.Exit(1)

    # Start Prometheus HTTP server
    start_http_server(port)
    typer.echo(f"Metrics available at http://localhost:{port}/metrics")

    # Collection loop
    while True:
        try:
            exporter_instance.collect()
        except Exception as e:
            typer.echo(f"Collection error: {e}", err=True)
        time.sleep(interval)


@app.command()
def status(
    chain: str = typer.Option("ethereum", help="Chain to check"),
) -> None:
    """Check node status (one-shot metrics collection).

    Examples:
        chainwatch status --chain ethereum
    """
    if chain == "ethereum":
        exporter_instance = EthereumExporter(settings.ethereum_rpc_url)
        typer.echo(f"Checking {chain} node at {settings.ethereum_rpc_url}...")
    else:
        typer.echo(f"Chain '{chain}' not supported yet")
        raise typer.Exit(1)

    try:
        exporter_instance.collect()
        typer.echo("Node Status: OK")
    except Exception as e:
        typer.echo(f"Node Status: ERROR - {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
