"""
Unit tests for updated NCAApiBaseClass.

Tests cover:
- Constructor works with and without api_version kwarg
- api_version defaults to "v1" when not specified
- endpoints property still returns NCAEndpoints instance
- router property returns ApiVersionRouter instance

Requirements: 1.1, 1.2, 4.1, 4.3
"""

from unittest.mock import MagicMock, patch

import pytest

from aplos_nca_saas_sdk.nca_resources._api_base import NCAApiBaseClass
from aplos_nca_saas_sdk.nca_resources.nca_endpoints import NCAEndpoints
from aplos_nca_saas_sdk.nca_resources.api_version_router import ApiVersionRouter


MOCK_AUTHENTICATOR = (
    "aplos_nca_saas_sdk.nca_resources._api_base.NCAAuthenticator"
)


class TestNCAApiBaseClassConstructor:
    """Test constructor works with and without api_version kwarg."""

    @patch(MOCK_AUTHENTICATOR)
    def test_constructor_without_api_version(self, mock_auth_cls: MagicMock) -> None:
        """Constructor should work without api_version (backward compat)."""
        base = NCAApiBaseClass("api.example.com")
        assert base.host == "api.example.com"
        mock_auth_cls.assert_called_once_with(host="api.example.com")

    @patch(MOCK_AUTHENTICATOR)
    def test_constructor_with_api_version_v1(self, mock_auth_cls: MagicMock) -> None:
        base = NCAApiBaseClass("api.example.com", api_version="v1")
        assert base.host == "api.example.com"
        assert base.api_version == "v1"

    @patch(MOCK_AUTHENTICATOR)
    def test_constructor_with_api_version_v3(self, mock_auth_cls: MagicMock) -> None:
        base = NCAApiBaseClass("api.example.com", api_version="v3")
        assert base.host == "api.example.com"
        assert base.api_version == "v3"

    def test_constructor_raises_on_empty_host(self) -> None:
        with pytest.raises(ValueError, match="Missing Aplos Api Domain"):
            NCAApiBaseClass("")


class TestNCAApiBaseClassApiVersion:
    """Test api_version defaults to 'v1' when not specified."""

    @patch(MOCK_AUTHENTICATOR)
    def test_defaults_to_v1_when_not_specified(self, mock_auth_cls: MagicMock) -> None:
        with patch.dict("os.environ", {}, clear=True):
            base = NCAApiBaseClass("api.example.com")
            assert base.api_version == "v1"

    @patch(MOCK_AUTHENTICATOR)
    def test_env_var_fallback(self, mock_auth_cls: MagicMock) -> None:
        """APLOS_API_VERSION env var should be used when no explicit version."""
        with patch.dict("os.environ", {"APLOS_API_VERSION": "v3"}):
            base = NCAApiBaseClass("api.example.com")
            assert base.api_version == "v3"

    @patch(MOCK_AUTHENTICATOR)
    def test_explicit_version_overrides_env_var(self, mock_auth_cls: MagicMock) -> None:
        with patch.dict("os.environ", {"APLOS_API_VERSION": "v3"}):
            base = NCAApiBaseClass("api.example.com", api_version="v1")
            assert base.api_version == "v1"


class TestNCAApiBaseClassEndpoints:
    """Test endpoints property still returns NCAEndpoints instance."""

    @patch(MOCK_AUTHENTICATOR)
    def test_endpoints_returns_nca_endpoints_instance(
        self, mock_auth_cls: MagicMock
    ) -> None:
        mock_cognito = MagicMock()
        mock_cognito.jwt = None  # No JWT set — triggers the falsy branch
        mock_auth_instance = MagicMock()
        mock_auth_instance.cognito = mock_cognito
        mock_auth_cls.return_value = mock_auth_instance

        base = NCAApiBaseClass("api.example.com")
        endpoints = base.endpoints
        assert isinstance(endpoints, NCAEndpoints)

    @patch(MOCK_AUTHENTICATOR)
    def test_endpoints_populates_ids_when_jwt_present(
        self, mock_auth_cls: MagicMock
    ) -> None:
        mock_cognito = MagicMock()
        mock_cognito.jwt = "fake-jwt-token"
        mock_cognito.tenant_id = "tenant-123"
        mock_cognito.user_id = "user-456"
        mock_auth_instance = MagicMock()
        mock_auth_instance.cognito = mock_cognito
        mock_auth_cls.return_value = mock_auth_instance

        base = NCAApiBaseClass("api.example.com")
        endpoints = base.endpoints
        assert isinstance(endpoints, NCAEndpoints)
        assert endpoints.tenant_id == "tenant-123"
        assert endpoints.user_id == "user-456"


class TestNCAApiBaseClassRouter:
    """Test router property returns ApiVersionRouter instance."""

    @patch(MOCK_AUTHENTICATOR)
    def test_router_returns_api_version_router(self, mock_auth_cls: MagicMock) -> None:
        base = NCAApiBaseClass("api.example.com", api_version="v1")
        router = base.router
        assert isinstance(router, ApiVersionRouter)

    @patch(MOCK_AUTHENTICATOR)
    def test_router_is_lazily_created(self, mock_auth_cls: MagicMock) -> None:
        """Router should not be created until .router is accessed."""
        base = NCAApiBaseClass("api.example.com", api_version="v1")
        # The private __router attribute should be None before first access
        assert base._NCAApiBaseClass__router is None  # type: ignore[attr-defined]

        _ = base.router
        assert base._NCAApiBaseClass__router is not None  # type: ignore[attr-defined]

    @patch(MOCK_AUTHENTICATOR)
    def test_router_cached_after_first_access(self, mock_auth_cls: MagicMock) -> None:
        base = NCAApiBaseClass("api.example.com", api_version="v1")
        first = base.router
        second = base.router
        assert first is second
