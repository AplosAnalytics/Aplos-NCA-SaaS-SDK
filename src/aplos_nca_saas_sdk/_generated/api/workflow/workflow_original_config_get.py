from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.success_envelope import SuccessEnvelope
from ...types import Response


def _get_kwargs(
    tenant_id: str,
    user_id: str,
    execution_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v3/tenants/{tenant_id}/users/{user_id}/executions/{execution_id}/config".format(
            tenant_id=quote(str(tenant_id), safe=""),
            user_id=quote(str(user_id), safe=""),
            execution_id=quote(str(execution_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | SuccessEnvelope | None:
    if response.status_code == 200:
        response_200 = SuccessEnvelope.from_dict(response.json())

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
) -> Response[ErrorEnvelope | SuccessEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    user_id: str,
    execution_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorEnvelope | SuccessEnvelope]:
    """Analysis Workflow: Original Config - Gets the original request config for an execution.

    Args:
        tenant_id (str):
        user_id (str):
        execution_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | SuccessEnvelope]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        user_id=user_id,
        execution_id=execution_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    user_id: str,
    execution_id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorEnvelope | SuccessEnvelope | None:
    """Analysis Workflow: Original Config - Gets the original request config for an execution.

    Args:
        tenant_id (str):
        user_id (str):
        execution_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | SuccessEnvelope
    """

    return sync_detailed(
        tenant_id=tenant_id,
        user_id=user_id,
        execution_id=execution_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    user_id: str,
    execution_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorEnvelope | SuccessEnvelope]:
    """Analysis Workflow: Original Config - Gets the original request config for an execution.

    Args:
        tenant_id (str):
        user_id (str):
        execution_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | SuccessEnvelope]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        user_id=user_id,
        execution_id=execution_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    user_id: str,
    execution_id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorEnvelope | SuccessEnvelope | None:
    """Analysis Workflow: Original Config - Gets the original request config for an execution.

    Args:
        tenant_id (str):
        user_id (str):
        execution_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | SuccessEnvelope
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            user_id=user_id,
            execution_id=execution_id,
            client=client,
        )
    ).parsed
