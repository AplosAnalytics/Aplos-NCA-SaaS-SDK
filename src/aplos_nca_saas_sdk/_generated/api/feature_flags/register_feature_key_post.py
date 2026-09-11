from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.feature_key_register_request import FeatureKeyRegisterRequest
from ...models.register_feature_key_post_response_201 import (
    RegisterFeatureKeyPostResponse201,
)
from ...types import Response


def _get_kwargs(
    *,
    body: FeatureKeyRegisterRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v3/feature-flags/register",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | RegisterFeatureKeyPostResponse201 | None:
    if response.status_code == 201:
        response_201 = RegisterFeatureKeyPostResponse201.from_dict(response.json())

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

    if response.status_code == 500:
        response_500 = ErrorEnvelope.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorEnvelope | RegisterFeatureKeyPostResponse201]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: FeatureKeyRegisterRequest,
) -> Response[ErrorEnvelope | RegisterFeatureKeyPostResponse201]:
    """Feature Flags: Register a new feature key (admin/dev)

    Args:
        body (FeatureKeyRegisterRequest): Request body to register (or update) a feature key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | RegisterFeatureKeyPostResponse201]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: FeatureKeyRegisterRequest,
) -> ErrorEnvelope | RegisterFeatureKeyPostResponse201 | None:
    """Feature Flags: Register a new feature key (admin/dev)

    Args:
        body (FeatureKeyRegisterRequest): Request body to register (or update) a feature key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | RegisterFeatureKeyPostResponse201
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: FeatureKeyRegisterRequest,
) -> Response[ErrorEnvelope | RegisterFeatureKeyPostResponse201]:
    """Feature Flags: Register a new feature key (admin/dev)

    Args:
        body (FeatureKeyRegisterRequest): Request body to register (or update) a feature key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | RegisterFeatureKeyPostResponse201]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: FeatureKeyRegisterRequest,
) -> ErrorEnvelope | RegisterFeatureKeyPostResponse201 | None:
    """Feature Flags: Register a new feature key (admin/dev)

    Args:
        body (FeatureKeyRegisterRequest): Request body to register (or update) a feature key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | RegisterFeatureKeyPostResponse201
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
