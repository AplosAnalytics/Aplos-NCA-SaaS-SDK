"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import os
from typing import Any

from aplos_nca_saas_sdk.nca_resources.api_client_factory import ApiClientFactory
from aplos_nca_saas_sdk.nca_resources.endpoint_strategy import EndpointStrategy


class ApiVersionRouter:
    """Selects the correct endpoint strategy based on configuration.

    Integrates with :class:`NCAAppConfiguration` for v3 ``api_routing``
    discovery.  The strategy is lazily created on first access so that
    network calls (v3 config fetch) are deferred until actually needed.
    """

    def __init__(self, *, host: str, api_version: str | None = None) -> None:
        self._host = host
        self._api_version = api_version or os.getenv("APLOS_API_VERSION", "v1")
        self._strategy: EndpointStrategy | None = None

    @property
    def strategy(self) -> EndpointStrategy:
        """Return the endpoint strategy, creating it on first access."""
        if self._strategy is None:
            kwargs: dict[str, Any] = {}
            if self._api_version == "v3":
                kwargs["api_routing"] = self._fetch_v3_routing()
            self._strategy = ApiClientFactory.create(self._api_version, **kwargs)
        return self._strategy

    def _fetch_v3_routing(self) -> dict[str, Any]:
        """Fetch ``api_routing`` from the v3 app configuration endpoint."""
        # Import here to avoid circular imports at module level.
        from aplos_nca_saas_sdk.nca_resources.nca_app_configuration import (
            NCAAppConfiguration,
        )

        config = NCAAppConfiguration(host=self._host, api_version="v3")
        return config.get_api_routing()
