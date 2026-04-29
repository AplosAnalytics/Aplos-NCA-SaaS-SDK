"""
Unit tests for V1EndpointStrategy.

Tests cover:
- Each v1 operation produces the correct URL with known tenant/user/resource IDs
- process_response() returns input unchanged
- version property returns "v1"

Requirements: 2.1, 2.3
"""

from typing import Any

from aplos_nca_saas_sdk.nca_resources.v1.endpoint_strategy import V1EndpointStrategy

HOST = "api.example.com"
TENANT_ID = "aaaa-bbbb-cccc-dddd"
USER_ID = "1111-2222-3333-4444"
RESOURCE_ID = "rrrr-ssss-tttt-uuuu"


class TestV1EndpointStrategyVersion:
    """Tests for the version property."""

    def test_version_returns_v1(self) -> None:
        strategy = V1EndpointStrategy()
        assert strategy.version == "v1"


class TestV1EndpointStrategyProcessResponse:
    """Tests for process_response passthrough."""

    def test_process_response_returns_input_unchanged(self) -> None:
        strategy = V1EndpointStrategy()
        data: dict[str, Any] = {"key": "value", "nested": {"a": 1}}
        assert strategy.process_response(data) is data

    def test_process_response_empty_dict(self) -> None:
        strategy = V1EndpointStrategy()
        data: dict[str, Any] = {}
        assert strategy.process_response(data) is data


class TestV1EndpointStrategyURLs:
    """Tests for get_endpoint_url with known IDs."""

    def setup_method(self) -> None:
        self.strategy = V1EndpointStrategy()

    def test_app_configuration(self) -> None:
        url = self.strategy.get_endpoint_url("app_configuration", host=HOST)
        assert url == f"https://{HOST}/app/configuration"

    def test_tenant(self) -> None:
        url = self.strategy.get_endpoint_url("tenant", host=HOST, tenant_id=TENANT_ID)
        assert url == f"https://{HOST}/tenants/{TENANT_ID}"

    def test_user(self) -> None:
        url = self.strategy.get_endpoint_url(
            "user", host=HOST, tenant_id=TENANT_ID, user_id=USER_ID
        )
        assert url == f"https://{HOST}/tenants/{TENANT_ID}/users/{USER_ID}"

    def test_executions(self) -> None:
        url = self.strategy.get_endpoint_url(
            "executions", host=HOST, tenant_id=TENANT_ID, user_id=USER_ID
        )
        assert url == f"https://{HOST}/tenants/{TENANT_ID}/users/{USER_ID}/nca/executions"

    def test_execution(self) -> None:
        url = self.strategy.get_endpoint_url(
            "execution",
            host=HOST,
            tenant_id=TENANT_ID,
            user_id=USER_ID,
            resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/tenants/{TENANT_ID}/users/{USER_ID}/nca/executions/{RESOURCE_ID}"

    def test_validations(self) -> None:
        url = self.strategy.get_endpoint_url(
            "validations", host=HOST, tenant_id=TENANT_ID, user_id=USER_ID
        )
        assert url == f"https://{HOST}/tenants/{TENANT_ID}/users/{USER_ID}/nca/validations"

    def test_validation(self) -> None:
        url = self.strategy.get_endpoint_url(
            "validation",
            host=HOST,
            tenant_id=TENANT_ID,
            user_id=USER_ID,
            resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/tenants/{TENANT_ID}/users/{USER_ID}/nca/validations/{RESOURCE_ID}"

    def test_files(self) -> None:
        url = self.strategy.get_endpoint_url(
            "files", host=HOST, tenant_id=TENANT_ID, user_id=USER_ID
        )
        assert url == f"https://{HOST}/tenants/{TENANT_ID}/users/{USER_ID}/nca/files"

    def test_file(self) -> None:
        url = self.strategy.get_endpoint_url(
            "file",
            host=HOST,
            tenant_id=TENANT_ID,
            user_id=USER_ID,
            resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/tenants/{TENANT_ID}/users/{USER_ID}/nca/files/{RESOURCE_ID}"

    def test_file_data(self) -> None:
        url = self.strategy.get_endpoint_url(
            "file_data",
            host=HOST,
            tenant_id=TENANT_ID,
            user_id=USER_ID,
            resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/tenants/{TENANT_ID}/users/{USER_ID}/nca/files/{RESOURCE_ID}/data"
