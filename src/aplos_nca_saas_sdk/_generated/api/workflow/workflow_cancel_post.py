from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.success_envelope import SuccessEnvelope
from ...models.workflow_cancel_post_body import WorkflowCancelPostBody
from ...types import Response


def _get_kwargs(
    tenant_id: str,
    user_id: str,
    execution_id: str,
    *,
    body: WorkflowCancelPostBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v3/tenants/{tenant_id}/users/{user_id}/executions/{execution_id}/cancel".format(
            tenant_id=quote(str(tenant_id), safe=""),
            user_id=quote(str(user_id), safe=""),
            execution_id=quote(str(execution_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | SuccessEnvelope | None:
    if response.status_code == 201:
        response_201 = SuccessEnvelope.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorEnvelope.from_dict(response.json())

        return response_400

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
    body: WorkflowCancelPostBody,
) -> Response[ErrorEnvelope | SuccessEnvelope]:
    """Analysis Workflow: Cancels workflow.

    Args:
        tenant_id (str):
        user_id (str):
        execution_id (str):
        body (WorkflowCancelPostBody):

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
        body=body,
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
    body: WorkflowCancelPostBody,
) -> ErrorEnvelope | SuccessEnvelope | None:
    """Analysis Workflow: Cancels workflow.

    Args:
        tenant_id (str):
        user_id (str):
        execution_id (str):
        body (WorkflowCancelPostBody):

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
        body=body,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    user_id: str,
    execution_id: str,
    *,
    client: AuthenticatedClient,
    body: WorkflowCancelPostBody,
) -> Response[ErrorEnvelope | SuccessEnvelope]:
    """Analysis Workflow: Cancels workflow.

    Args:
        tenant_id (str):
        user_id (str):
        execution_id (str):
        body (WorkflowCancelPostBody):

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
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    user_id: str,
    execution_id: str,
    *,
    client: AuthenticatedClient,
    body: WorkflowCancelPostBody,
) -> ErrorEnvelope | SuccessEnvelope | None:
    """Analysis Workflow: Cancels workflow.

    Args:
        tenant_id (str):
        user_id (str):
        execution_id (str):
        body (WorkflowCancelPostBody):

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
            body=body,
        )
    ).parsed
