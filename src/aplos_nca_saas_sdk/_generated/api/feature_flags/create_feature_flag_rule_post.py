from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_feature_flag_rule_post_response_201 import (
    CreateFeatureFlagRulePostResponse201,
)
from ...models.error_envelope import ErrorEnvelope
from ...models.feature_flag_rule_create_request import FeatureFlagRuleCreateRequest
from ...types import Response


def _get_kwargs(
    *,
    body: FeatureFlagRuleCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v3/feature-flags/rules",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateFeatureFlagRulePostResponse201 | ErrorEnvelope | None:
    if response.status_code == 201:
        response_201 = CreateFeatureFlagRulePostResponse201.from_dict(response.json())

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
) -> Response[CreateFeatureFlagRulePostResponse201 | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: FeatureFlagRuleCreateRequest,
) -> Response[CreateFeatureFlagRulePostResponse201 | ErrorEnvelope]:
    """Feature Flags: Create a flag rule (admin)

    Args:
        body (FeatureFlagRuleCreateRequest): Request body to create a feature-flag rule.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateFeatureFlagRulePostResponse201 | ErrorEnvelope]
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
    body: FeatureFlagRuleCreateRequest,
) -> CreateFeatureFlagRulePostResponse201 | ErrorEnvelope | None:
    """Feature Flags: Create a flag rule (admin)

    Args:
        body (FeatureFlagRuleCreateRequest): Request body to create a feature-flag rule.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateFeatureFlagRulePostResponse201 | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: FeatureFlagRuleCreateRequest,
) -> Response[CreateFeatureFlagRulePostResponse201 | ErrorEnvelope]:
    """Feature Flags: Create a flag rule (admin)

    Args:
        body (FeatureFlagRuleCreateRequest): Request body to create a feature-flag rule.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateFeatureFlagRulePostResponse201 | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: FeatureFlagRuleCreateRequest,
) -> CreateFeatureFlagRulePostResponse201 | ErrorEnvelope | None:
    """Feature Flags: Create a flag rule (admin)

    Args:
        body (FeatureFlagRuleCreateRequest): Request body to create a feature-flag rule.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateFeatureFlagRulePostResponse201 | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
