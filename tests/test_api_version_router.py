"""
Unit tests for ApiRoutingConfig and ApiVersionRouter.

Tests cover:
- ApiRoutingConfig.from_dict() with complete, partial, and empty routing dicts
- ApiVersionRouter creates v1 strategy without config fetch
- ApiVersionRouter creates v3 strategy with mocked config fetch

Requirements: 1.1, 1.2, 1.3, 11.2
"""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

# Ensure v1 and v3 strategies are registered
import aplos_nca_saas_sdk.nca_resources.v1  # noqa: F401
import aplos_nca_saas_sdk.nca_resources.v3  # noqa: F401
from aplos_nca_saas_sdk.nca_resources.api_version_router import ApiVersionRouter
from aplos_nca_saas_sdk.nca_resources.v1.endpoint_strategy import V1EndpointStrategy
from aplos_nca_saas_sdk.nca_resources.v3.endpoint_strategy import (
    ApiRoutingConfig,
    V3EndpointStrategy,
)


class TestApiRoutingConfigFromDict:
    """Tests for ApiRoutingConfig.from_dict()."""

    def test_complete_routing_dict(self) -> None:
        routing = {
            "users": {"version": "v3"},
            "tenants": {"version": "v1"},
            "subscriptions": {"version": "v3"},
            "site_messages": {"version": "v2"},
            "metrics": {"version": "v3"},
        }
        config = ApiRoutingConfig.from_dict(routing)
        assert config.users == "v3"
        assert config.tenants == "v1"
        assert config.subscriptions == "v3"
        assert config.site_messages == "v2"
        assert config.metrics == "v3"

    def test_partial_routing_dict_missing_domains(self) -> None:
        routing = {
            "users": {"version": "v1"},
            "tenants": {"version": "v3"},
        }
        config = ApiRoutingConfig.from_dict(routing)
        assert config.users == "v1"
        assert config.tenants == "v3"
        assert config.subscriptions == "v3"  # default
        assert config.site_messages == "v3"  # default
        assert config.metrics == "v3"  # default

    def test_empty_routing_dict(self) -> None:
        config = ApiRoutingConfig.from_dict({})
        assert config.users == "v3"
        assert config.tenants == "v3"
        assert config.subscriptions == "v3"
        assert config.site_messages == "v3"
        assert config.metrics == "v3"

    def test_non_dict_domain_values_default_to_v3(self) -> None:
        routing: dict[str, Any] = {
            "users": "not-a-dict",
            "tenants": 42,
            "subscriptions": None,
            "site_messages": ["list"],
            "metrics": True,
        }
        config = ApiRoutingConfig.from_dict(routing)
        assert config.users == "v3"
        assert config.tenants == "v3"
        assert config.subscriptions == "v3"
        assert config.site_messages == "v3"
        assert config.metrics == "v3"

    def test_dict_without_version_key_defaults_to_v3(self) -> None:
        routing = {
            "users": {"other_key": "value"},
            "tenants": {},
        }
        config = ApiRoutingConfig.from_dict(routing)
        assert config.users == "v3"
        assert config.tenants == "v3"

    def test_mixed_valid_and_invalid_entries(self) -> None:
        routing: dict[str, Any] = {
            "users": {"version": "v1"},
            "tenants": "invalid",
            "subscriptions": {"version": "v5"},
            # site_messages and metrics absent
        }
        config = ApiRoutingConfig.from_dict(routing)
        assert config.users == "v1"
        assert config.tenants == "v3"
        assert config.subscriptions == "v5"
        assert config.site_messages == "v3"
        assert config.metrics == "v3"


MOCK_NCA_APP_CONFIG = (
    "aplos_nca_saas_sdk.nca_resources.nca_app_configuration.NCAAppConfiguration"
)


class TestApiVersionRouterV1:
    """Tests for ApiVersionRouter with v1."""

    def test_v1_creates_strategy_without_config_fetch(self) -> None:
        """V1 should not call NCAAppConfiguration at all."""
        with patch(MOCK_NCA_APP_CONFIG) as mock_config_cls:
            router = ApiVersionRouter(host="api.example.com", api_version="v1")
            strategy = router.strategy

            assert isinstance(strategy, V1EndpointStrategy)
            assert strategy.version == "v1"
            mock_config_cls.assert_not_called()

    def test_v1_default_when_no_version_specified(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with patch(MOCK_NCA_APP_CONFIG) as mock_config_cls:
                router = ApiVersionRouter(host="api.example.com")
                strategy = router.strategy

                assert isinstance(strategy, V1EndpointStrategy)
                mock_config_cls.assert_not_called()


class TestApiVersionRouterV3:
    """Tests for ApiVersionRouter with v3."""

    def test_v3_fetches_config_and_passes_api_routing(self) -> None:
        """V3 should fetch config and pass api_routing to the factory."""
        mock_routing = {
            "users": {"version": "v3"},
            "tenants": {"version": "v3"},
        }

        mock_config_instance = MagicMock()
        mock_config_instance.get_api_routing.return_value = mock_routing

        with patch(
            MOCK_NCA_APP_CONFIG,
            return_value=mock_config_instance,
        ) as mock_config_cls:
            router = ApiVersionRouter(host="api.example.com", api_version="v3")
            strategy = router.strategy

            assert isinstance(strategy, V3EndpointStrategy)
            assert strategy.version == "v3"
            mock_config_cls.assert_called_once_with(
                host="api.example.com", api_version="v3"
            )
            mock_config_instance.get_api_routing.assert_called_once()

    def test_v3_strategy_receives_routing_data(self) -> None:
        """Verify the V3 strategy is initialized with the routing data."""
        mock_routing = {
            "users": {"version": "v1"},
            "metrics": {"version": "v3"},
        }

        mock_config_instance = MagicMock()
        mock_config_instance.get_api_routing.return_value = mock_routing

        with patch(
            MOCK_NCA_APP_CONFIG,
            return_value=mock_config_instance,
        ):
            router = ApiVersionRouter(host="api.example.com", api_version="v3")
            strategy = router.strategy

            # The strategy should have been created with the routing data
            assert isinstance(strategy, V3EndpointStrategy)
            assert strategy._api_routing == mock_routing

    def test_v3_strategy_is_lazily_created(self) -> None:
        """Strategy should not be created until .strategy is accessed."""
        with patch(MOCK_NCA_APP_CONFIG) as mock_config_cls:
            router = ApiVersionRouter(host="api.example.com", api_version="v3")

            # Config should not be fetched yet
            mock_config_cls.assert_not_called()

            # Now access strategy
            mock_config_instance = MagicMock()
            mock_config_instance.get_api_routing.return_value = {}
            mock_config_cls.return_value = mock_config_instance

            _ = router.strategy
            mock_config_cls.assert_called_once()

    def test_v3_strategy_cached_after_first_access(self) -> None:
        """Subsequent .strategy accesses should return the same instance."""
        mock_config_instance = MagicMock()
        mock_config_instance.get_api_routing.return_value = {}

        with patch(
            MOCK_NCA_APP_CONFIG,
            return_value=mock_config_instance,
        ):
            router = ApiVersionRouter(host="api.example.com", api_version="v3")
            first = router.strategy
            second = router.strategy

            assert first is second
            # Config should only be fetched once
            mock_config_instance.get_api_routing.assert_called_once()
