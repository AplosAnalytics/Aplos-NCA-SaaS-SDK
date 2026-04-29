"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from dataclasses import dataclass
from typing import Any

from aplos_nca_saas_sdk.nca_resources.v3.diagnostic_envelope import (
    DiagnosticEnvelopeHandler,
)


@dataclass
class ApiRoutingConfig:
    """Parsed api_routing from /v3/app/configuration.

    Each field holds the version string for its corresponding API domain,
    defaulting to ``"v3"`` when the domain is absent from the configuration.
    """

    users: str = "v3"
    tenants: str = "v3"
    subscriptions: str = "v3"
    site_messages: str = "v3"
    metrics: str = "v3"

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "ApiRoutingConfig":
        """Create an :class:`ApiRoutingConfig` from a raw ``api_routing`` dict.

        For each domain the method looks for a nested ``{"version": "..."}``
        mapping and falls back to ``"v3"`` when the domain key is missing or
        the value is not a dict.
        """
        return cls(
            users=(
                d.get("users", {}).get("version", "v3")
                if isinstance(d.get("users"), dict)
                else "v3"
            ),
            tenants=(
                d.get("tenants", {}).get("version", "v3")
                if isinstance(d.get("tenants"), dict)
                else "v3"
            ),
            subscriptions=(
                d.get("subscriptions", {}).get("version", "v3")
                if isinstance(d.get("subscriptions"), dict)
                else "v3"
            ),
            site_messages=(
                d.get("site_messages", {}).get("version", "v3")
                if isinstance(d.get("site_messages"), dict)
                else "v3"
            ),
            metrics=(
                d.get("metrics", {}).get("version", "v3")
                if isinstance(d.get("metrics"), dict)
                else "v3"
            ),
        )


class V3EndpointStrategy:
    """V3 endpoint strategy with domain-based routing and envelope handling.

    All URL templates use the ``/v3/`` version prefix.  Responses are
    automatically unwrapped through :class:`DiagnosticEnvelopeHandler`.
    """

    # Maps each operation to its API domain for routing purposes.
    DOMAIN_MAP: dict[str, str | None] = {
        "user": "users",
        "executions": "users",
        "execution": "users",
        "analysis_queue": "users",
        "execution_status": "users",
        "execution_config": "users",
        "execution_outputs_package": "users",
        "execution_outputs_report": "users",
        "execution_cancel": "users",
        "execution_archive": "users",
        "execution_output_by_type": "users",
        "validations": "users",
        "validation": "users",
        "files": "users",
        "file": "users",
        "file_data": "users",
        "file_download_url": "users",
        "file_stream": "users",
        "file_lineage": "users",
        "file_meta": "users",
        "file_archive": "users",
        "file_unarchive": "users",
        "assignable_roles": "users",
        "tenant": "tenants",
        "tenant_subscriptions": "subscriptions",
        "update_subscription": "subscriptions",
        "user_metrics": "metrics",
        "tenant_metrics": "metrics",
        "public_messages": "site_messages",
        "user_messages": "site_messages",
        "company_logos": "site_messages",
        "app_configuration": None,  # no domain routing
    }

    OPERATIONS: dict[str, str] = {
        "app_configuration": "/v3/app/configuration",
        "tenant": "/v3/tenants/{tenant_id}",
        "user": "/v3/tenants/{tenant_id}/users/{user_id}",
        "executions": "/v3/tenants/{tenant_id}/users/{user_id}/nca/executions",
        "execution": "/v3/tenants/{tenant_id}/users/{user_id}/nca/executions/{resource_id}",
        "analysis_queue": "/v3/tenants/{tenant_id}/users/{user_id}/analysis/queue",
        "execution_status": "/v3/tenants/{tenant_id}/users/{user_id}/executions/{resource_id}/status",
        "execution_config": "/v3/tenants/{tenant_id}/users/{user_id}/executions/{resource_id}/config",
        "execution_outputs_package": "/v3/tenants/{tenant_id}/users/{user_id}/executions/{resource_id}/outputs/package",
        "execution_outputs_report": "/v3/tenants/{tenant_id}/users/{user_id}/executions/{resource_id}/outputs/report",
        "execution_cancel": "/v3/tenants/{tenant_id}/users/{user_id}/executions/{resource_id}/cancel",
        "execution_archive": "/v3/tenants/{tenant_id}/users/{user_id}/executions/{resource_id}/archive",
        "execution_output_by_type": "/v3/tenants/{tenant_id}/users/{user_id}/executions/{resource_id}/outputs/type/{sub_resource}",
        "validations": "/v3/tenants/{tenant_id}/users/{user_id}/nca/validations",
        "validation": "/v3/tenants/{tenant_id}/users/{user_id}/nca/validations/{resource_id}",
        "files": "/v3/tenants/{tenant_id}/users/{user_id}/files",
        "file": "/v3/tenants/{tenant_id}/users/{user_id}/files/{resource_id}",
        "file_download_url": "/v3/tenants/{tenant_id}/users/{user_id}/files/{resource_id}/download-url",
        "file_stream": "/v3/tenants/{tenant_id}/users/{user_id}/files/{resource_id}/stream",
        "file_lineage": "/v3/tenants/{tenant_id}/users/{user_id}/files/{resource_id}/lineage",
        "file_meta": "/v3/tenants/{tenant_id}/users/{user_id}/files/{resource_id}/meta",
        "file_archive": "/v3/tenants/{tenant_id}/users/{user_id}/files/{resource_id}/archive",
        "file_unarchive": "/v3/tenants/{tenant_id}/users/{user_id}/files/{resource_id}/unarchive",
        "tenant_subscriptions": "/v3/tenants/{tenant_id}/subscriptions",
        "update_subscription": "/v3/tenants/{tenant_id}/subscriptions/{resource_id}",
        "user_metrics": "/v3/tenants/{tenant_id}/users/{user_id}/metrics",
        "tenant_metrics": "/v3/tenants/{tenant_id}/metrics",
        "public_messages": "/v3/app/messages",
        "user_messages": "/v3/tenants/{tenant_id}/users/{user_id}/messages",
        "company_logos": "/v3/app/company-logos",
        "assignable_roles": "/v3/tenants/{tenant_id}/users/{user_id}/assignable-roles",
    }

    def __init__(self, *, api_routing: dict[str, Any] | None = None) -> None:
        self._api_routing = api_routing or {}
        self._route_prefixes: dict[str, str] = {}
        self._parse_routing()

    def _parse_routing(self) -> None:
        """Derive per-domain route prefixes from api_routing config."""
        for domain, settings in self._api_routing.items():
            version = (
                settings.get("version", "v3")
                if isinstance(settings, dict)
                else "v3"
            )
            self._route_prefixes[domain] = f"/{version}"

    @property
    def version(self) -> str:
        """Return the version identifier."""
        return "v3"

    def get_endpoint_url(
        self,
        operation: str,
        *,
        host: str,
        tenant_id: str | None = None,
        user_id: str | None = None,
        resource_id: str | None = None,
        sub_resource: str | None = None,
    ) -> str:
        """Construct the full URL for a given logical operation."""
        template = self.OPERATIONS[operation]
        url = f"https://{host}{template}"
        return url.format(
            tenant_id=tenant_id,
            user_id=user_id,
            resource_id=resource_id,
            sub_resource=sub_resource,
        )

    def process_response(self, response_data: dict[str, Any]) -> dict[str, Any]:
        """Unwrap the v3 diagnostic envelope, if present."""
        return DiagnosticEnvelopeHandler.unwrap(response_data)
