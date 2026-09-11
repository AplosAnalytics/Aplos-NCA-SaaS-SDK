"""Offline facade tests for AplosClient.

Uses httpx.MockTransport (no network, no dev dependency) to exercise a
representative set of endpoints end-to-end through the facade:
- auth header is attached (bearer token),
- the correct v3 URL is called,
- the success envelope is unwrapped to the typed entity,
- an error envelope raises AplosApiError.
"""

from __future__ import annotations

import json

import httpx
import pytest

from aplos_nca_saas_sdk.client import AplosClient, AplosApiError


def _mock_client(handler) -> AplosClient:
    """Build an AplosClient whose transport uses a MockTransport handler.

    We inject the mock transport via ``httpx_args`` so the generated
    AuthenticatedClient still constructs its own httpx.Client — which is what
    attaches the bearer Authorization header. (Replacing the whole client with
    set_httpx_client would bypass that header injection.)
    """
    from aplos_nca_saas_sdk._generated.client import AuthenticatedClient

    client = AplosClient(
        host="api.test.aplos-nca.com",
        token="test.jwt.token",
        tenant_id="t-1",
        user_id="u-1",
        verify_ssl=False,
    )
    client._transport = AuthenticatedClient(
        base_url="https://api.test.aplos-nca.com/api",
        token="test.jwt.token",
        verify_ssl=False,
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    return client


def test_get_user_unwraps_to_typed_entity():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["auth"] = request.headers.get("Authorization")
        body = {
            "success": True,
            "statusCode": 200,
            "timestamp": "2026-01-01T00:00:00Z",
            "data": {
                "id": "u-1",
                "tenantId": "t-1",
                "email": "me@example.com",
                "firstName": "Ada",
                "roles": ["tenant_user"],
            },
        }
        return httpx.Response(200, json=body)

    client = _mock_client(handler)
    user = client.users.get("u-1")

    # Correct v3 URL + bearer auth attached
    assert (
        captured["url"] == "https://api.test.aplos-nca.com/api/v3/tenants/t-1/users/u-1"
    )
    assert captured["auth"] == "Bearer test.jwt.token"
    # Envelope unwrapped to the typed entity
    assert user.id == "u-1"
    assert user.email == "me@example.com"
    assert user.first_name == "Ada"


def test_list_users_returns_pagination_payload():
    def handler(request: httpx.Request) -> httpx.Response:
        body = {
            "success": True,
            "statusCode": 200,
            "timestamp": "2026-01-01T00:00:00Z",
            "data": {
                "count": 1,
                "nextKey": None,
                "users": [{"id": "u-1", "tenantId": "t-1", "email": "a@b.com"}],
            },
        }
        return httpx.Response(200, json=body)

    client = _mock_client(handler)
    payload = client.users.list()
    assert payload.count == 1
    assert payload.users[0].email == "a@b.com"


def test_workflow_status_unwraps_execution():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/executions/exec-9/status")
        body = {
            "success": True,
            "statusCode": 200,
            "timestamp": "2026-01-01T00:00:00Z",
            "data": {"id": "exec-9", "status": "succeeded", "workflowType": "nca"},
        }
        return httpx.Response(200, json=body)

    client = _mock_client(handler)
    execution = client.workflow.status("exec-9")
    assert execution.id == "exec-9"
    assert execution.status == "succeeded"


def test_error_envelope_raises_aplos_api_error():
    def handler(request: httpx.Request) -> httpx.Response:
        body = {
            "success": False,
            "statusCode": 404,
            "timestamp": "2026-01-01T00:00:00Z",
            "error": {"message": "Resource not found", "code": "NOT_FOUND"},
        }
        return httpx.Response(404, json=body)

    client = _mock_client(handler)
    with pytest.raises(AplosApiError) as exc_info:
        client.users.get("missing")
    err = exc_info.value
    assert err.code == "NOT_FOUND"
    assert err.status_code == 404
    assert "not found" in err.message.lower()


def test_transport_required_without_auth():
    """Accessing a domain op before auth raises a clear error."""
    client = AplosClient(host="api.test.aplos-nca.com")  # no token, no login
    with pytest.raises(RuntimeError):
        _ = client.transport
