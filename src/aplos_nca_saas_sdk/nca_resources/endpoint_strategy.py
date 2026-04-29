"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Any, Protocol


class EndpointStrategy(Protocol):
    """Contract for version-specific endpoint construction and response handling.

    Each API version (v1, v3, etc.) implements this protocol to provide
    version-appropriate URL construction and response processing.
    """

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
        ...

    def process_response(self, response_data: dict[str, Any]) -> dict[str, Any]:
        """Process/unwrap the API response according to version conventions."""
        ...

    @property
    def version(self) -> str:
        """Return the version identifier (e.g., 'v1', 'v3')."""
        ...
