"""
Unit tests for updated NCAAppConfiguration.

Tests cover:
- v1 config URL matches existing behavior
- v3 config URL uses /v3/app/configuration
- get_api_routing() extracts routing map from mocked v3 response
- RuntimeError raised when v3 config endpoint returns non-200
- Cognito extraction unchanged for both v1 and v3

Requirements: 11.1, 11.2, 11.3, 11.4
"""

from unittest.mock import MagicMock, patch

import pytest

from aplos_nca_saas_sdk.nca_resources.nca_app_configuration import NCAAppConfiguration


HOST = "api.example.com"


def _mock_response(status_code: int = 200, json_data: dict | None = None) -> MagicMock:
    """Create a mock requests.Response."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data or {}
    return resp


class TestConfigUrl:
    """Tests for config_url property."""

    def test_v1_config_url_matches_existing_behavior(self) -> None:
        config = NCAAppConfiguration(host=HOST)
        assert config.config_url == f"https://{HOST}/app/configuration"

    def test_v1_explicit_config_url(self) -> None:
        config = NCAAppConfiguration(host=HOST, api_version="v1")
        assert config.config_url == f"https://{HOST}/app/configuration"

    def test_v3_config_url(self) -> None:
        config = NCAAppConfiguration(host=HOST, api_version="v3")
        assert config.config_url == f"https://{HOST}/v3/app/configuration"


class TestGetApiRouting:
    """Tests for get_api_routing() method."""

    def test_extracts_routing_map_from_v3_response(self) -> None:
        routing_data = {
            "users": {"version": "v3"},
            "tenants": {"version": "v3"},
            "subscriptions": {"version": "v1"},
        }
        mock_resp = _mock_response(json_data={"api_routing": routing_data, "idp": {}})

        with patch("requests.get", return_value=mock_resp):
            config = NCAAppConfiguration(host=HOST, api_version="v3")
            result = config.get_api_routing()

        assert result == routing_data

    def test_returns_empty_dict_when_api_routing_absent(self) -> None:
        mock_resp = _mock_response(json_data={"idp": {}})

        with patch("requests.get", return_value=mock_resp):
            config = NCAAppConfiguration(host=HOST, api_version="v3")
            result = config.get_api_routing()

        assert result == {}


class TestRuntimeErrorOnNon200:
    """Tests for RuntimeError when config endpoint returns non-200."""

    def test_raises_runtime_error_on_non_200_v3(self) -> None:
        mock_resp = _mock_response(status_code=500)

        with patch("requests.get", return_value=mock_resp):
            config = NCAAppConfiguration(host=HOST, api_version="v3")
            with pytest.raises(RuntimeError, match="App configuration endpoint failed"):
                config.get()

    def test_raises_runtime_error_on_non_200_v1(self) -> None:
        mock_resp = _mock_response(status_code=404)

        with patch("requests.get", return_value=mock_resp):
            config = NCAAppConfiguration(host=HOST, api_version="v1")
            with pytest.raises(RuntimeError, match="App configuration endpoint failed"):
                config.get()

    def test_error_message_includes_url_and_status(self) -> None:
        mock_resp = _mock_response(status_code=503)

        with patch("requests.get", return_value=mock_resp):
            config = NCAAppConfiguration(host=HOST, api_version="v3")
            with pytest.raises(RuntimeError, match=r"status 503"):
                config.get()


class TestCognitoExtraction:
    """Tests for Cognito extraction unchanged for both v1 and v3."""

    COGNITO_RESPONSE = {
        "idp": {
            "Auth": {
                "Cognito": {
                    "userPoolClientId": "test-client-id-123",
                    "region": "us-west-2",
                    "userPoolId": "us-west-2_ABC123",
                    "authenticationFlowType": "USER_SRP_AUTH",
                }
            }
        }
    }

    def test_cognito_client_id_v1(self) -> None:
        mock_resp = _mock_response(json_data=self.COGNITO_RESPONSE)

        with patch("requests.get", return_value=mock_resp):
            config = NCAAppConfiguration(host=HOST)
            assert config.cognito_client_id == "test-client-id-123"

    def test_cognito_region_v1(self) -> None:
        mock_resp = _mock_response(json_data=self.COGNITO_RESPONSE)

        with patch("requests.get", return_value=mock_resp):
            config = NCAAppConfiguration(host=HOST)
            assert config.cognito_region == "us-west-2"

    def test_cognito_client_id_v3(self) -> None:
        mock_resp = _mock_response(json_data=self.COGNITO_RESPONSE)

        with patch("requests.get", return_value=mock_resp):
            config = NCAAppConfiguration(host=HOST, api_version="v3")
            assert config.cognito_client_id == "test-client-id-123"

    def test_cognito_region_v3(self) -> None:
        mock_resp = _mock_response(json_data=self.COGNITO_RESPONSE)

        with patch("requests.get", return_value=mock_resp):
            config = NCAAppConfiguration(host=HOST, api_version="v3")
            assert config.cognito_region == "us-west-2"

    def test_cognito_extraction_identical_for_v1_and_v3(self) -> None:
        """Both v1 and v3 should extract the same Cognito values."""
        mock_resp_v1 = _mock_response(json_data=self.COGNITO_RESPONSE)
        mock_resp_v3 = _mock_response(json_data=self.COGNITO_RESPONSE)

        with patch("requests.get", return_value=mock_resp_v1):
            config_v1 = NCAAppConfiguration(host=HOST, api_version="v1")
            v1_client_id = config_v1.cognito_client_id
            v1_region = config_v1.cognito_region

        with patch("requests.get", return_value=mock_resp_v3):
            config_v3 = NCAAppConfiguration(host=HOST, api_version="v3")
            v3_client_id = config_v3.cognito_client_id
            v3_region = config_v3.cognito_region

        assert v1_client_id == v3_client_id
        assert v1_region == v3_region
