from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.audit_logs_query_by_resource_get_response_200 import (
    AuditLogsQueryByResourceGetResponse200,
)
from ...models.error_envelope import ErrorEnvelope
from ...types import Response


def _get_kwargs(
    tenant_id: str,
    resource_type: str,
    resource_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v3/tenants/{tenant_id}/audit-logs/resources/{resource_type}/{resource_id}".format(
            tenant_id=quote(str(tenant_id), safe=""),
            resource_type=quote(str(resource_type), safe=""),
            resource_id=quote(str(resource_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AuditLogsQueryByResourceGetResponse200 | ErrorEnvelope | None:
    if response.status_code == 200:
        response_200 = AuditLogsQueryByResourceGetResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorEnvelope.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorEnvelope.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorEnvelope.from_dict(response.json())

        return response_404

    if response.status_code == 500:
        response_500 = ErrorEnvelope.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AuditLogsQueryByResourceGetResponse200 | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    resource_type: str,
    resource_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[AuditLogsQueryByResourceGetResponse200 | ErrorEnvelope]:
    """Audit Logs: Query audit log entries for a specific resource

    Args:
        tenant_id (str):
        resource_type (str):
        resource_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditLogsQueryByResourceGetResponse200 | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        resource_type=resource_type,
        resource_id=resource_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    resource_type: str,
    resource_id: str,
    *,
    client: AuthenticatedClient,
) -> AuditLogsQueryByResourceGetResponse200 | ErrorEnvelope | None:
    """Audit Logs: Query audit log entries for a specific resource

    Args:
        tenant_id (str):
        resource_type (str):
        resource_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuditLogsQueryByResourceGetResponse200 | ErrorEnvelope
    """

    return sync_detailed(
        tenant_id=tenant_id,
        resource_type=resource_type,
        resource_id=resource_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    resource_type: str,
    resource_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[AuditLogsQueryByResourceGetResponse200 | ErrorEnvelope]:
    """Audit Logs: Query audit log entries for a specific resource

    Args:
        tenant_id (str):
        resource_type (str):
        resource_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditLogsQueryByResourceGetResponse200 | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        resource_type=resource_type,
        resource_id=resource_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    resource_type: str,
    resource_id: str,
    *,
    client: AuthenticatedClient,
) -> AuditLogsQueryByResourceGetResponse200 | ErrorEnvelope | None:
    """Audit Logs: Query audit log entries for a specific resource

    Args:
        tenant_id (str):
        resource_type (str):
        resource_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuditLogsQueryByResourceGetResponse200 | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            resource_type=resource_type,
            resource_id=resource_id,
            client=client,
        )
    ).parsed
