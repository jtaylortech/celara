"""Tests for CLI commands."""

from pathlib import Path

from typer.testing import CliRunner

from daoform.cli import app

runner = CliRunner()


def test_init(tmp_path) -> None:
    output = str(tmp_path / "dao.yaml")
    result = runner.invoke(app, ["init", "--name", "TestDAO", "--output", output])
    assert result.exit_code == 0
    assert "Created" in result.stdout
    assert Path(output).exists()


def test_validate(tmp_path) -> None:
    output = str(tmp_path / "dao.yaml")
    runner.invoke(app, ["init", "--name", "TestDAO", "--output", output])
    result = runner.invoke(app, ["validate", "--config-file", output])
    assert result.exit_code == 0
    assert "Valid" in result.stdout


def test_validate_bad_file(tmp_path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("not: valid: dao: config: [")
    result = runner.invoke(app, ["validate", "--config-file", str(bad)])
    assert result.exit_code == 1
