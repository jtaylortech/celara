"""ChainOps CLI."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from chainops.config import ChainOpsConfig
from chainops.deployer import Deployer

app = typer.Typer(help="ChainOps - Infrastructure-as-Code for validators")
console = Console()


@app.command()
def init(
    chain: str = typer.Argument(..., help="Blockchain (ethereum, solana)"),
    network: str = typer.Option("mainnet", help="Network (mainnet, testnet, sepolia)"),
    provider: str = typer.Option("aws", help="Cloud provider (aws, gcp, azure)"),
    region: str = typer.Option("us-east-1", help="Cloud region"),
    name: str = typer.Option(None, help="Validator name"),
) -> None:
    """Initialize validator configuration."""
    if name is None:
        name = f"{chain}-validator"

    console.print(f"[bold blue]Initializing {chain} validator on {network}...[/bold blue]")

    config = ChainOpsConfig(
        name=name,
        chain=chain,  # type: ignore
        network=network,  # type: ignore
        provider=provider,  # type: ignore
        region=region,
    )

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

    # Simple cost estimation (AWS us-east-1)
    costs = {
        "EC2 Instance": 120.0,  # t3.xlarge
        "EBS Storage": 160.0,  # 2TB gp3
        "Data Transfer": 45.0,  # ~500GB/month
        "CloudWatch": 10.0,
    }

    if config.compute.spot_instances:
        costs["EC2 Instance"] = 36.0  # 70% savings

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


if __name__ == "__main__":
    app()
