"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Any, Dict

import requests
from aws_lambda_powertools import Logger

from aplos_nca_saas_sdk.nca_resources._api_base import NCAApiBaseClass
from aplos_nca_saas_sdk.utilities.http_utility import HttpUtilities

logger = Logger()


class NCATenantUserManagement(NCAApiBaseClass):
    """V3 Tenant and User Management API.

    Provides methods for tenant info, user info, subscriptions,
    metrics, messages, company logos, and assignable roles.
    All operations route through :class:`V3EndpointStrategy` and
    responses are processed through the diagnostic envelope handler.
    """

    def __init__(self, host: str) -> None:
        super().__init__(host)

    # ------------------------------------------------------------------
    # V3 helpers
    # ------------------------------------------------------------------

    def _get_v3_url(
        self,
        operation: str,
        *,
        resource_id: str | None = None,
        sub_resource: str | None = None,
    ) -> str:
        """Build a v3 endpoint URL via the router strategy."""
        return self.router.strategy.get_endpoint_url(
            operation,
            host=self.host,
            tenant_id=self.authenticator.cognito.tenant_id,
            user_id=self.authenticator.cognito.user_id,
            resource_id=resource_id,
            sub_resource=sub_resource,
        )

    def _process_v3_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Unwrap a v3 diagnostic envelope via the router strategy."""
        return self.router.strategy.process_response(response_data)

    # ------------------------------------------------------------------
    # Tenant operations
    # ------------------------------------------------------------------

    def get_tenant(self) -> Dict[str, Any]:
        """Retrieve tenant information (v3).

        Calls GET ``/v3/tenants/{tenant_id}`` using the ``tenants``
        domain route prefix.

        Returns:
            The (unwrapped) tenant information response.
        """
        url = self._get_v3_url("tenant")
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving tenant info.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get tenant info: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def get_tenant_metrics(self) -> Dict[str, Any]:
        """Retrieve tenant-level metrics (v3).

        Calls GET ``/v3/tenants/{tenant_id}/metrics`` using the
        ``metrics`` domain route prefix.

        Returns:
            The (unwrapped) tenant metrics response.
        """
        url = self._get_v3_url("tenant_metrics")
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving tenant metrics.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get tenant metrics: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    # ------------------------------------------------------------------
    # Subscription operations
    # ------------------------------------------------------------------

    def get_tenant_subscriptions(self) -> Dict[str, Any]:
        """Retrieve tenant subscription list (v3).

        Calls GET ``/v3/tenants/{tenant_id}/subscriptions`` using the
        ``subscriptions`` domain route prefix.

        Returns:
            The (unwrapped) subscriptions response.
        """
        url = self._get_v3_url("tenant_subscriptions")
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError(
                "403 Forbidden when retrieving tenant subscriptions."
            )
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get tenant subscriptions: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def update_subscription(
        self, subscription_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a tenant subscription (v3).

        Calls PUT ``/v3/tenants/{tenant_id}/subscriptions/{subscription_id}``
        using the ``subscriptions`` domain route prefix.

        Args:
            subscription_id: The subscription identifier.
            payload: The subscription update payload.

        Returns:
            The (unwrapped) update response.
        """
        url = self._get_v3_url("update_subscription", resource_id=subscription_id)
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.put(
            url, headers=headers, json=payload, timeout=30
        )

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when updating subscription.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to update subscription: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    # ------------------------------------------------------------------
    # User operations
    # ------------------------------------------------------------------

    def get_user(self) -> Dict[str, Any]:
        """Retrieve user information (v3).

        Calls GET ``/v3/tenants/{tenant_id}/users/{user_id}`` using the
        ``users`` domain route prefix.

        Returns:
            The (unwrapped) user information response.
        """
        url = self._get_v3_url("user")
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving user info.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get user info: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def get_user_metrics(self) -> Dict[str, Any]:
        """Retrieve user-level metrics (v3).

        Calls GET ``/v3/tenants/{tenant_id}/users/{user_id}/metrics``
        using the ``metrics`` domain route prefix.

        Returns:
            The (unwrapped) user metrics response.
        """
        url = self._get_v3_url("user_metrics")
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving user metrics.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get user metrics: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def get_user_messages(self) -> Dict[str, Any]:
        """Retrieve user messages (v3).

        Calls GET ``/v3/tenants/{tenant_id}/users/{user_id}/messages``
        using the ``site_messages`` domain route prefix.

        Returns:
            The (unwrapped) user messages response.
        """
        url = self._get_v3_url("user_messages")
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving user messages.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get user messages: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def get_assignable_roles(self) -> Dict[str, Any]:
        """Retrieve assignable roles for the current user (v3).

        Calls GET ``/v3/tenants/{tenant_id}/users/{user_id}/assignable-roles``
        using the ``users`` domain route prefix.

        Returns:
            The (unwrapped) assignable roles response.
        """
        url = self._get_v3_url("assignable_roles")
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving assignable roles.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get assignable roles: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    # ------------------------------------------------------------------
    # Site-wide operations
    # ------------------------------------------------------------------

    def get_public_messages(self) -> Dict[str, Any]:
        """Retrieve public site messages (v3).

        Calls GET ``/v3/app/messages`` using the ``site_messages``
        domain route prefix.

        Returns:
            The (unwrapped) public messages response.
        """
        url = self._get_v3_url("public_messages")
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving public messages.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get public messages: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def get_company_logos(self) -> Dict[str, Any]:
        """Retrieve company logos (v3).

        Calls GET ``/v3/app/company-logos`` using the ``site_messages``
        domain route prefix.

        Returns:
            The (unwrapped) company logos response.
        """
        url = self._get_v3_url("company_logos")
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving company logos.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get company logos: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())
