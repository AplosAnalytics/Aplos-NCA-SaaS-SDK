"""
Unit tests for EndpointStrategy protocol and ApiClientFactory.

Tests cover:
- Factory creates correct strategy for "v1" and "v3" after registration
- Env var fallback when no explicit version provided
- Explicit version overrides env var
- ValueError for unsupported version strings
- register() adds new version without modifying existing entries

Requirements: 1.1, 1.2, 1.4, 1.5, 3.1, 3.5
"""

import os
from typing import Any
from unittest.mock import patch

import pytest

# Ensure v1 and v3 strategies are registered
import aplos_nca_saas_sdk.nca_resources.v1  # noqa: F401
import aplos_nca_saas_sdk.nca_resources.v3  # noqa: F401
from aplos_nca_saas_sdk.nca_resources.api_client_factory import ApiClientFactory
from aplos_nca_saas_sdk.nca_resources.v1.endpoint_strategy import V1EndpointStrategy
from aplos_nca_saas_sdk.nca_resources.v3.endpoint_strategy import V3EndpointStrategy


class TestApiClientFactoryCreate:
    """Tests for ApiClientFactory.create()."""

    def test_create_v1_returns_v1_strategy(self) -> None:
        strategy = ApiClientFactory.create("v1")
        assert isinstance(strategy, V1EndpointStrategy)
        assert strategy.version == "v1"

    def test_create_v3_returns_v3_strategy(self) -> None:
        strategy = ApiClientFactory.create("v3")
        assert isinstance(strategy, V3EndpointStrategy)
        assert strategy.version == "v3"

    def test_unsupported_version_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Unsupported api_version 'v99'"):
            ApiClientFactory.create("v99")

    def test_unsupported_version_message_lists_supported(self) -> None:
        with pytest.raises(ValueError, match="Supported versions:") as exc_info:
            ApiClientFactory.create("nope")
        msg = str(exc_info.value)
        assert "v1" in msg
        assert "v3" in msg

    def test_empty_string_falls_back_to_default(self) -> None:
        # Empty string is falsy, so factory treats it as "no version" and defaults to v1
        strategy = ApiClientFactory.create("")
        assert strategy.version == "v1"


class TestApiClientFactoryEnvVar:
    """Tests for APLOS_API_VERSION env var fallback."""

    def test_env_var_fallback_to_v3(self) -> None:
        with patch.dict(os.environ, {"APLOS_API_VERSION": "v3"}):
            strategy = ApiClientFactory.create()
        assert strategy.version == "v3"

    def test_env_var_fallback_to_v1(self) -> None:
        with patch.dict(os.environ, {"APLOS_API_VERSION": "v1"}):
            strategy = ApiClientFactory.create()
        assert strategy.version == "v1"

    def test_no_env_var_defaults_to_v1(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            strategy = ApiClientFactory.create()
        assert strategy.version == "v1"

    def test_explicit_version_overrides_env_var(self) -> None:
        with patch.dict(os.environ, {"APLOS_API_VERSION": "v3"}):
            strategy = ApiClientFactory.create("v1")
        assert strategy.version == "v1"

    def test_explicit_v3_overrides_env_v1(self) -> None:
        with patch.dict(os.environ, {"APLOS_API_VERSION": "v1"}):
            strategy = ApiClientFactory.create("v3")
        assert strategy.version == "v3"


class TestApiClientFactoryRegister:
    """Tests for ApiClientFactory.register()."""

    def test_register_adds_new_version(self) -> None:
        class MockStrategy:
            @property
            def version(self) -> str:
                return "v99"

            def get_endpoint_url(self, operation: str, **kwargs: Any) -> str:
                return ""

            def process_response(self, response_data: dict[str, Any]) -> dict[str, Any]:
                return response_data

        # Save original registry state
        original_registry = dict(ApiClientFactory._registry)
        try:
            ApiClientFactory.register("v99", MockStrategy)
            strategy = ApiClientFactory.create("v99")
            assert strategy.version == "v99"
        finally:
            # Restore original registry
            ApiClientFactory._registry = original_registry

    def test_register_does_not_modify_existing_entries(self) -> None:
        class AnotherMock:
            @property
            def version(self) -> str:
                return "v50"

            def get_endpoint_url(self, operation: str, **kwargs: Any) -> str:
                return ""

            def process_response(self, response_data: dict[str, Any]) -> dict[str, Any]:
                return response_data

        original_registry = dict(ApiClientFactory._registry)
        try:
            # v1 and v3 should still work after registering v50
            ApiClientFactory.register("v50", AnotherMock)

            v1 = ApiClientFactory.create("v1")
            assert isinstance(v1, V1EndpointStrategy)

            v3 = ApiClientFactory.create("v3")
            assert isinstance(v3, V3EndpointStrategy)

            v50 = ApiClientFactory.create("v50")
            assert v50.version == "v50"
        finally:
            ApiClientFactory._registry = original_registry
