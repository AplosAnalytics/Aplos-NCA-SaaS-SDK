"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import os
from typing import Any

from aplos_nca_saas_sdk.nca_resources.endpoint_strategy import EndpointStrategy


class ApiClientFactory:
    """Creates version-specific endpoint strategies.

    Maintains a registry of API version strings to strategy classes.
    New versions are added via ``register()`` without modifying existing code.
    """

    _registry: dict[str, type[EndpointStrategy]] = {}

    @classmethod
    def register(cls, version: str, strategy_class: type[EndpointStrategy]) -> None:
        """Register a strategy class for a given API version."""
        cls._registry[version] = strategy_class

    @classmethod
    def create(
        cls, version: str | None = None, **kwargs: Any
    ) -> EndpointStrategy:
        """Create an endpoint strategy for the given version.

        Falls back to the ``APLOS_API_VERSION`` environment variable,
        then defaults to ``"v1"``.
        """
        resolved_version = version or os.getenv("APLOS_API_VERSION", "v1")
        if resolved_version not in cls._registry:
            supported = ", ".join(sorted(cls._registry.keys()))
            raise ValueError(
                f"Unsupported api_version '{resolved_version}'. "
                f"Supported versions: {supported}"
            )
        return cls._registry[resolved_version](**kwargs)
