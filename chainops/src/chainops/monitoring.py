"""Monitoring configuration for validators."""

from pathlib import Path


def get_prometheus_config(chain: str, validator_name: str) -> str:
    """Generate Prometheus scrape config for a validator."""
    if chain == "ethereum":
        return f"""# Prometheus scrape config for {validator_name}
scrape_configs:
  - job_name: '{validator_name}-geth'
    static_configs:
      - targets: ['localhost:6060']
    metrics_path: /debug/metrics/prometheus

  - job_name: '{validator_name}-beacon'
    static_configs:
      - targets: ['localhost:5054']
"""
    elif chain == "solana":
        return f"""# Prometheus scrape config for {validator_name}
scrape_configs:
  - job_name: '{validator_name}-solana'
    static_configs:
      - targets: ['localhost:9090']
"""
    return ""


def get_cloudwatch_agent_config(chain: str, validator_name: str) -> dict:
    """Generate CloudWatch agent config."""
    base_config = {
        "agent": {"metrics_collection_interval": 60, "run_as_user": "root"},
        "metrics": {
            "namespace": f"ChainOps/{validator_name}",
            "metrics_collected": {
                "cpu": {"measurement": ["cpu_usage_idle", "cpu_usage_user", "cpu_usage_system"]},
                "disk": {"measurement": ["used_percent"], "resources": ["/", "/data"]},
                "mem": {"measurement": ["mem_used_percent"]},
                "net": {"measurement": ["bytes_sent", "bytes_recv"]},
            },
        },
        "logs": {
            "logs_collected": {
                "files": {
                    "collect_list": [
                        {
                            "file_path": f"/var/log/{chain}/*.log",
                            "log_group_name": f"/chainops/{validator_name}",
                            "log_stream_name": "{instance_id}/{hostname}",
                        }
                    ]
                }
            }
        },
    }

    if chain == "ethereum":
        base_config["logs"]["logs_collected"]["files"]["collect_list"].append(
            {
                "file_path": "/var/log/syslog",
                "log_group_name": f"/chainops/{validator_name}",
                "log_stream_name": "geth-syslog",
                "filters": [{"type": "include", "expression": "geth"}],
            }
        )
    elif chain == "solana":
        base_config["logs"]["logs_collected"]["files"]["collect_list"].append(
            {
                "file_path": "/var/log/syslog",
                "log_group_name": f"/chainops/{validator_name}",
                "log_stream_name": "solana-syslog",
                "filters": [{"type": "include", "expression": "solana"}],
            }
        )

    return base_config


def generate_monitoring_files(chain: str, validator_name: str, output_dir: Path) -> None:
    """Generate monitoring config files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Prometheus config
    prom_config = get_prometheus_config(chain, validator_name)
    (output_dir / "prometheus.yml").write_text(prom_config)

    # CloudWatch agent config
    import json

    cw_config = get_cloudwatch_agent_config(chain, validator_name)
    (output_dir / "cloudwatch-agent.json").write_text(json.dumps(cw_config, indent=2))
