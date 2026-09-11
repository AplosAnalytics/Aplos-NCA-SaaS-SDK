from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.feature_key_register_request import FeatureKeyRegisterRequest
from ...models.update_feature_key_put_response_200 import UpdateFeatureKeyPutResponse200
from ...types import Response


def _get_kwargs(
    registration_id: str,
    *,
    body: FeatureKeyRegisterRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v3/feature-flags/registry/{registration_id}".format(
            registration_id=quote(str(registration_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | UpdateFeatureKeyPutResponse200 | None:
    if response.status_code == 200:
        response_200 = UpdateFeatureKeyPutResponse200.from_dict(response.json())

        return response_200

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
) -> Response[ErrorEnvelope | UpdateFeatureKeyPutResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    registration_id: str,
    *,
    client: AuthenticatedClient,
    body: FeatureKeyRegisterRequest,
) -> Response[ErrorEnvelope | UpdateFeatureKeyPutResponse200]:
    """Feature Flags: Update a feature key registration (admin/dev)

    Args:
        registration_id (str):
        body (FeatureKeyRegisterRequest): Request body to register (or update) a feature key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | UpdateFeatureKeyPutResponse200]
    """

    kwargs = _get_kwargs(
        registration_id=registration_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    registration_id: str,
    *,
    client: AuthenticatedClient,
    body: FeatureKeyRegisterRequest,
) -> ErrorEnvelope | UpdateFeatureKeyPutResponse200 | None:
    """Feature Flags: Update a feature key registration (admin/dev)

    Args:
        registration_id (str):
        body (FeatureKeyRegisterRequest): Request body to register (or update) a feature key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | UpdateFeatureKeyPutResponse200
    """

    return sync_detailed(
        registration_id=registration_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    registration_id: str,
    *,
    client: AuthenticatedClient,
    body: FeatureKeyRegisterRequest,
) -> Response[ErrorEnvelope | UpdateFeatureKeyPutResponse200]:
    """Feature Flags: Update a feature key registration (admin/dev)

    Args:
        registration_id (str):
        body (FeatureKeyRegisterRequest): Request body to register (or update) a feature key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | UpdateFeatureKeyPutResponse200]
    """

    kwargs = _get_kwargs(
        registration_id=registration_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    registration_id: str,
    *,
    client: AuthenticatedClient,
    body: FeatureKeyRegisterRequest,
) -> ErrorEnvelope | UpdateFeatureKeyPutResponse200 | None:
    """Feature Flags: Update a feature key registration (admin/dev)

    Args:
        registration_id (str):
        body (FeatureKeyRegisterRequest): Request body to register (or update) a feature key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | UpdateFeatureKeyPutResponse200
    """

    return (
        await asyncio_detailed(
            registration_id=registration_id,
            client=client,
            body=body,
        )
    ).parsed
