"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import os
from typing import Any

from aplos_nca_saas_sdk.nca_resources.nca_authenticator import NCAAuthenticator
from aplos_nca_saas_sdk.nca_resources.nca_endpoints import NCAEndpoints


class NCAApiBaseClass:
    """NCA Api Base Class — updated with optional api_version support."""

    def __init__(self, host: str, *, api_version: str | None = None) -> None:
        self.host = host
        if not host:
            raise ValueError("Missing Aplos Api Domain")
        self.__authenticator: NCAAuthenticator = NCAAuthenticator(host=host)
        self.__endpoints: NCAEndpoints = NCAEndpoints(host=host)
        self.__api_version = api_version
        self.__router: Any = None  # lazy-initialized ApiVersionRouter

    @property
    def api_version(self) -> str:
        """Return the resolved API version.

        Uses the explicit value passed to the constructor, falls back to
        the ``APLOS_API_VERSION`` environment variable, and finally
        defaults to ``"v1"``.
        """
        return self.__api_version or os.getenv("APLOS_API_VERSION", "v1")

    @property
    def router(self) -> "ApiVersionRouter":  # noqa: F821
        """Return the :class:`ApiVersionRouter`, creating it on first access."""
        if self.__router is None:
            from aplos_nca_saas_sdk.nca_resources.api_version_router import (
                ApiVersionRouter,
            )

            self.__router = ApiVersionRouter(
                host=self.host, api_version=self.__api_version
            )
        return self.__router

    @property
    def authenticator(self) -> NCAAuthenticator:
        """Gets the authenticator"""

        return self.__authenticator

    @authenticator.setter
    def authenticator(self, value: Any) -> None:
        """Sets the authenticator"""

        self.__authenticator = value

    @property
    def endpoints(self) -> NCAEndpoints:
        """Gets the endpoints"""

        if self.authenticator.cognito.jwt:
            self.__endpoints.tenant_id = self.authenticator.cognito.tenant_id
            self.__endpoints.user_id = self.authenticator.cognito.user_id

        return self.__endpoints
