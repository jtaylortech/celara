"""ChainOps CLI."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from chainops.config import ChainOpsConfig
from chainops.deployer import Deployer
from chainops.state import State

app = typer.Typer(help="ChainOps - Infrastructure-as-Code for validators")
console = Console()

# Chain-specific defaults
CHAIN_DEFAULTS = {
    "ethereum": {"instance_type": "t3.xlarge", "storage_size": 2000},
    "solana": {"instance_type": "r6i.2xlarge", "storage_size": 2000},
}


@app.command()
def init(
    chain: str = typer.Argument(..., help="Blockchain (ethereum, solana)"),
    network: str = typer.Option("mainnet", help="Network (mainnet, testnet, sepolia, devnet)"),
    provider: str = typer.Option("aws", help="Cloud provider (aws)"),
    region: str = typer.Option("us-east-1", help="Cloud region"),
    name: str = typer.Option(None, help="Validator name"),
) -> None:
    """Initialize validator configuration."""
    if chain not in CHAIN_DEFAULTS:
        console.print(f"[red]Error:[/red] Unsupported chain: {chain}")
        console.print(f"Supported chains: {', '.join(CHAIN_DEFAULTS.keys())}")
        raise typer.Exit(1)

    if name is None:
        name = f"{chain}-validator"

    console.print(f"[bold blue]Initializing {chain} validator on {network}...[/bold blue]")

    defaults = CHAIN_DEFAULTS[chain]
    config = ChainOpsConfig(
        name=name,
        chain=chain,  # type: ignore
        network=network,  # type: ignore
        provider=provider,  # type: ignore
        region=region,
    )
    config.compute.instance_type = defaults["instance_type"]
    config.compute.storage_size = defaults["storage_size"]

    config_path = Path("chainops.yaml")
    config.save(config_path)

    console.print(f"[green]✓[/green] Configuration saved to {config_path}")
    console.print("\n[bold]Next steps:[/bold]")
    console.print("  1. Review and customize: [cyan]vim chainops.yaml[/cyan]")
    console.print("  2. Estimate costs: [cyan]chainops estimate[/cyan]")
    console.print("  3. Deploy: [cyan]chainops deploy[/cyan]")


@app.command()
def deploy(
    config_file: Path = typer.Option("chainops.yaml", help="Config file"),
    auto_approve: bool = typer.Option(False, "--auto-approve", help="Skip confirmation"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show plan without deploying"),
) -> None:
    """Deploy validator infrastructure."""
    if not config_file.exists():
        console.print(f"[red]Error:[/red] Config file not found: {config_file}")
        console.print("Run [cyan]chainops init[/cyan] first")
        raise typer.Exit(1)

    config = ChainOpsConfig.load(config_file)
    deployer = Deployer(config)

    console.print(f"[bold blue]Deploying {config.name}...[/bold blue]")

    if dry_run:
        console.print("[yellow]Dry run mode - showing plan only[/yellow]")
        deployer.plan()
        return

    if not auto_approve:
        table = Table(title="Deployment Summary")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Chain", config.chain)
        table.add_row("Network", config.network)
        table.add_row("Provider", config.provider)
        table.add_row("Region", config.region)
        table.add_row("Instance Type", config.compute.instance_type)
        table.add_row("Storage", f"{config.compute.storage_size} GB")
        console.print(table)

        if not typer.confirm("\nDeploy infrastructure?"):
            raise typer.Abort()

    deployer.deploy()
    console.print("[green]✓[/green] Validator deployed successfully")


@app.command()
def status(
    config_file: Path = typer.Option("chainops.yaml", help="Config file"),
) -> None:
    """Check validator status."""
    if not config_file.exists():
        console.print(f"[red]Error:[/red] Config file not found: {config_file}")
        raise typer.Exit(1)

    config = ChainOpsConfig.load(config_file)
    deployer = Deployer(config)

    console.print(f"[bold]Validator Status: {config.name}[/bold]\n")
    status_info = deployer.status()

    table = Table()
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    for key, value in status_info.items():
        table.add_row(key, str(value))

    console.print(table)


@app.command()
def destroy(
    config_file: Path = typer.Option("chainops.yaml", help="Config file"),
    force: bool = typer.Option(False, "--force", help="Skip confirmation"),
) -> None:
    """Destroy validator infrastructure."""
    if not config_file.exists():
        console.print(f"[red]Error:[/red] Config file not found: {config_file}")
        raise typer.Exit(1)

    config = ChainOpsConfig.load(config_file)
    deployer = Deployer(config)

    console.print(f"[bold red]Destroying {config.name}...[/bold red]")

    if not force:
        console.print("[yellow]Warning:[/yellow] This will destroy all infrastructure")
        if not typer.confirm("Are you sure?"):
            raise typer.Abort()

    deployer.destroy()
    console.print("[green]✓[/green] Infrastructure destroyed")


@app.command()
def estimate(
    config_file: Path = typer.Option("chainops.yaml", help="Config file"),
) -> None:
    """Estimate monthly costs."""
    if not config_file.exists():
        console.print(f"[red]Error:[/red] Config file not found: {config_file}")
        raise typer.Exit(1)

    config = ChainOpsConfig.load(config_file)

    console.print(f"[bold]Cost Estimate: {config.name}[/bold]\n")

    # Chain-specific cost estimation
    if config.chain == "ethereum":
        costs = {
            "EC2 Instance (t3.xlarge)": 120.0,
            "EBS Storage (2TB gp3)": 160.0,
            "Data Transfer (~500GB)": 45.0,
            "CloudWatch": 10.0,
        }
        if config.compute.spot_instances:
            costs["EC2 Instance (t3.xlarge)"] = 36.0
    elif config.chain == "solana":
        costs = {
            "EC2 Instance (r6i.2xlarge)": 360.0,
            "EBS Ledger (2TB gp3 high IOPS)": 200.0,
            "EBS Accounts (500GB gp3)": 50.0,
            "Data Transfer (~1TB)": 90.0,
            "CloudWatch": 15.0,
        }
        if config.compute.spot_instances:
            costs["EC2 Instance (r6i.2xlarge)"] = 108.0
    else:
        costs = {"Compute": 200.0, "Storage": 100.0, "Network": 50.0}

    table = Table(title="Monthly Cost Estimate (USD)")
    table.add_column("Component", style="cyan")
    table.add_column("Cost", style="green", justify="right")

    total = 0.0
    for component, cost in costs.items():
        table.add_row(component, f"${cost:.2f}")
        total += cost

    table.add_row("[bold]Total[/bold]", f"[bold]${total:.2f}[/bold]")
    console.print(table)

    if config.compute.spot_instances:
        console.print("\n[green]✓[/green] Spot instances enabled (70% savings)")


@app.command("list")
def list_deployments() -> None:
    """List all tracked deployments."""
    state = State.load()
    deployments = state.list_all()

    if not deployments:
        console.print("[yellow]No deployments found.[/yellow]")
        console.print("Run [cyan]chainops init[/cyan] and [cyan]chainops deploy[/cyan] to create one.")
        return

    table = Table(title="ChainOps Deployments")
    table.add_column("Name", style="cyan")
    table.add_column("Chain", style="blue")
    table.add_column("Network", style="blue")
    table.add_column("Status", style="green")
    table.add_column("Public IP", style="yellow")
    table.add_column("Region", style="dim")

    for d in deployments:
        status_color = {
            "running": "green",
            "deploying": "yellow",
            "stopped": "dim",
            "destroyed": "red",
            "failed": "red",
        }.get(d.status, "white")

        table.add_row(
            d.name,
            d.chain,
            d.network,
            f"[{status_color}]{d.status}[/{status_color}]",
            d.public_ip or "N/A",
            d.region,
        )

    console.print(table)


if __name__ == "__main__":
    app()
