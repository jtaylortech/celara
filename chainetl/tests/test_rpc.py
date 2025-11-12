"""Tests for RPC client."""

import httpx
import pytest

from chainetl.utils.rpc import RPCClient


def test_rpc_call_success(monkeypatch) -> None:
    client = RPCClient("http://example.test")

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {"result": "0x1"}

    monkeypatch.setattr(client.client, "post", lambda url, json: FakeResponse())

    result = client.call("eth_blockNumber", [])
    assert result == "0x1"


def test_rpc_call_rpc_error(monkeypatch) -> None:
    client = RPCClient("http://example.test")

    class FakeErrorResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {"error": {"message": "bad request"}}

    monkeypatch.setattr(client.client, "post", lambda url, json: FakeErrorResponse())

    with pytest.raises(ValueError, match="RPC error: bad request"):
        client.call("some_method", [])


def test_rpc_call_http_error(monkeypatch) -> None:
    client = RPCClient("http://example.test")

    def raise_http_error(url, json):
        raise httpx.HTTPError("network")

    monkeypatch.setattr(client.client, "post", raise_http_error)

    with pytest.raises(httpx.HTTPError):
        client.call("eth_blockNumber", [])
