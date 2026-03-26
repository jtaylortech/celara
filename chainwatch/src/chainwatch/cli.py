"""Command-line interface."""

import time

import typer
from prometheus_client import start_http_server

from chainwatch.config import SUPPORTED_CHAINS, settings
from chainwatch.exporters.evm import EVMExporter

app = typer.Typer(help="ChainWatch - Observability for decentralized systems")


def _get_exporter(chain: str) -> EVMExporter:
    """Create exporter for the given chain."""
    if chain not in SUPPORTED_CHAINS:
        chain_list = ", ".join(SUPPORTED_CHAINS)
        typer.echo(
            f"❌ Unsupported chain: '{chain}'. Supported: {chain_list}",
            err=True,
        )
        raise typer.Exit(1)
    rpc_url = getattr(settings, SUPPORTED_CHAINS[chain])
    return EVMExporter(rpc_url, chain=chain)


@app.command()
def exporter(
    chain: str = typer.Option("ethereum", help="Chain to monitor"),
    port: int = typer.Option(settings.exporter_port, help="Metrics port"),
    interval: int = typer.Option(
        settings.scrape_interval, help="Scrape interval (seconds)"
    ),
) -> None:
    """Run Prometheus metrics exporter."""
    exp = _get_exporter(chain)
    typer.echo(f"Starting {chain} exporter on port {port}")
    typer.echo(f"RPC: {exp.rpc_url}")

    start_http_server(port)
    typer.echo(f"Metrics at http://localhost:{port}/metrics")

    while True:
        try:
            exp.collect()
        except Exception as e:
            typer.echo(f"Collection error: {e}", err=True)
        time.sleep(interval)


@app.command()
def status(
    chain: str = typer.Option("ethereum", help="Chain to check"),
) -> None:
    """One-shot node health check."""
    exp = _get_exporter(chain)
    typer.echo(f"Checking {chain} node at {exp.rpc_url}...")

    try:
        exp.collect()
        typer.echo("Node Status: OK")
    except Exception as e:
        typer.echo(f"Node Status: ERROR - {e}")
        raise typer.Exit(1)


@app.command()
def chains() -> None:
    """List supported blockchains."""
    typer.echo("Supported chains:")
    for name in SUPPORTED_CHAINS:
        rpc_url = getattr(settings, SUPPORTED_CHAINS[name])
        typer.echo(f"  • {name:12s} {rpc_url}")


if __name__ == "__main__":
    app()
