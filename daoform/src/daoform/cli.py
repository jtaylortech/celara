"""Command-line interface."""

import typer
import yaml

from daoform.engine import GovernanceEngine
from daoform.models import DAOConfig, Proposal, ProposalStatus

app = typer.Typer(help="DAOForm - Governance-as-Code for DAOs")


@app.command()
def init(
    name: str = typer.Option(..., help="DAO name"),
    output: str = typer.Option("dao.yaml", help="Output config file"),
) -> None:
    """Initialize a new DAO governance config."""
    config = DAOConfig(name=name)
    data = config.model_dump(mode="json")
    with open(output, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
    typer.echo(f"Created {output} for '{name}'")
    typer.echo(f"  Quorum: {config.quorum * 100}%")
    typer.echo(f"  Threshold: {config.threshold * 100}%")
    typer.echo(f"  Voting period: {config.voting_period_days} days")


@app.command()
def validate(
    config_file: str = typer.Option("dao.yaml", help="Config file"),
) -> None:
    """Validate a DAO governance config."""
    try:
        with open(config_file) as f:
            data = yaml.safe_load(f)
        config = DAOConfig(**data)
        typer.echo(f"✅ Valid config for '{config.name}'")
    except Exception as e:
        typer.echo(f"❌ Invalid config: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def propose(
    config_file: str = typer.Option("dao.yaml", help="Config file"),
    title: str = typer.Option(..., help="Proposal title"),
    author: str = typer.Option(..., help="Author"),
    proposal_id: str = typer.Option(..., "--id", help="Proposal ID"),
) -> None:
    """Create a new governance proposal."""
    with open(config_file) as f:
        config = DAOConfig(**yaml.safe_load(f))
    engine = GovernanceEngine(config)
    proposal = engine.create_proposal(
        Proposal(id=proposal_id, title=title, author=author)
    )
    typer.echo(f"Created proposal: {proposal.id}")
    typer.echo(f"  Title: {proposal.title}")
    typer.echo(f"  Status: {proposal.status.value}")


if __name__ == "__main__":
    app()
