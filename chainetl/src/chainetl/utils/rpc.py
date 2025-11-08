"""JSON-RPC client for blockchain nodes."""

from typing import Any

import httpx
import structlog

logger = structlog.get_logger()


class RPCClient:
    """JSON-RPC client."""

    def __init__(self, url: str, timeout: float = 30.0) -> None:
        """Initialize RPC client.

        Args:
            url: RPC endpoint URL
            timeout: Request timeout in seconds
        """
        self.url = url
        self.client = httpx.Client(timeout=timeout)

    def call(self, method: str, params: list[Any]) -> Any:
        """Make JSON-RPC call.

        Args:
            method: RPC method name
            params: Method parameters

        Returns:
            RPC result

        Raises:
            ValueError: If RPC returns an error
            httpx.HTTPError: If HTTP request fails
        """
        payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}

        try:
            response = self.client.post(self.url, json=payload)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                error_msg = data["error"].get("message", str(data["error"]))
                raise ValueError(f"RPC error: {error_msg}")

            return data["result"]

        except httpx.HTTPError as e:
            logger.error("rpc_call_failed", method=method, url=self.url, error=str(e))
            raise

    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self) -> "RPCClient":
        """Context manager entry."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.close()
