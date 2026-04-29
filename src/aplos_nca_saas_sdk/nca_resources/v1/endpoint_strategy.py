"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Any


class V1EndpointStrategy:
    """V1 (unversioned) endpoint strategy — mirrors current NCAEndpoints behavior.

    All URL templates use the existing unversioned paths (no ``/v1/`` prefix).
    Responses are returned unchanged (passthrough).
    """

    OPERATIONS: dict[str, str] = {
        "app_configuration": "/app/configuration",
        "tenant": "/tenants/{tenant_id}",
        "user": "/tenants/{tenant_id}/users/{user_id}",
        "executions": "/tenants/{tenant_id}/users/{user_id}/nca/executions",
        "execution": "/tenants/{tenant_id}/users/{user_id}/nca/executions/{resource_id}",
        "validations": "/tenants/{tenant_id}/users/{user_id}/nca/validations",
        "validation": "/tenants/{tenant_id}/users/{user_id}/nca/validations/{resource_id}",
        "files": "/tenants/{tenant_id}/users/{user_id}/nca/files",
        "file": "/tenants/{tenant_id}/users/{user_id}/nca/files/{resource_id}",
        "file_data": "/tenants/{tenant_id}/users/{user_id}/nca/files/{resource_id}/data",
    }

    @property
    def version(self) -> str:
        """Return the version identifier."""
        return "v1"

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
        """Return the response unchanged (passthrough for v1)."""
        return response_data
