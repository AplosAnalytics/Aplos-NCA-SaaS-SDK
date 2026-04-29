"""
Unit tests for updated resource classes (Task 8.6).

Tests cover:
- NCAAnalysis v3 methods produce correct endpoint URLs (mocked HTTP)
- NCAFileUpload and NCAFileDownload v3 methods produce correct endpoint URLs
- NCAValidation v3 routing
- NCATenantUserManagement operations produce correct endpoint URLs
- All resource classes still work with v1 defaults (backward compatibility)
- V3 responses are unwrapped through diagnostic envelope handler

Requirements: 4.1, 4.2, 6.1–6.8, 7.1–7.8, 8.1–8.8
"""

from unittest.mock import MagicMock, patch

import pytest

from aplos_nca_saas_sdk.nca_resources.v3.endpoint_strategy import V3EndpointStrategy
from aplos_nca_saas_sdk.nca_resources.v1.endpoint_strategy import V1EndpointStrategy

# ---------------------------------------------------------------------------
# Shared constants / helpers
# ---------------------------------------------------------------------------

HOST = "api.example.com"
TENANT_ID = "tenant-aaa"
USER_ID = "user-bbb"
RESOURCE_ID = "res-ccc"
FAKE_JWT = "fake-jwt-token"

MOCK_AUTH = "aplos_nca_saas_sdk.nca_resources._api_base.NCAAuthenticator"

# A minimal v3 envelope response used across tests
ENVELOPE_RESPONSE = {
    "data": {"result": "ok"},
    "statusCode": 200,
    "timestamp": "2025-01-01T00:00:00Z",
    "success": True,
    "diagnostics": {"duration": 42},
}

# Expected unwrapped payload from the envelope above
UNWRAPPED = {"result": "ok", "_diagnostics": {"duration": 42}}


def _make_mock_cognito() -> MagicMock:
    """Return a mock cognito object with tenant/user IDs and JWT."""
    cognito = MagicMock()
    cognito.tenant_id = TENANT_ID
    cognito.user_id = USER_ID
    cognito.jwt = FAKE_JWT
    return cognito


def _make_mock_auth(cognito: MagicMock | None = None) -> MagicMock:
    """Return a mock authenticator instance."""
    auth = MagicMock()
    auth.cognito = cognito or _make_mock_cognito()
    auth.get_jwt_http_headers.return_value = {"Authorization": f"Bearer {FAKE_JWT}"}
    return auth


def _make_v3_strategy() -> V3EndpointStrategy:
    return V3EndpointStrategy()


def _make_v1_strategy() -> V1EndpointStrategy:
    return V1EndpointStrategy()


def _mock_router(strategy):
    """Return a mock router whose .strategy is the given strategy."""
    router = MagicMock()
    router.strategy = strategy
    return router


def _make_http_response(status_code: int = 200, json_data: dict | None = None):
    """Return a mock requests.Response."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.reason = "OK" if status_code == 200 else "Error"
    resp.json.return_value = json_data or ENVELOPE_RESPONSE
    return resp


# ===================================================================
# NCAAnalysis tests
# ===================================================================

class TestNCAAnalysisV3Endpoints:
    """Test NCAAnalysis v3 methods produce correct endpoint URLs."""

    @patch(MOCK_AUTH)
    def test_execution_status_url(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_analysis import NCAAnalysis

        analysis = NCAAnalysis(HOST)
        analysis._NCAApiBaseClass__api_version = "v3"
        strategy = _make_v3_strategy()
        analysis._NCAApiBaseClass__router = _mock_router(strategy)

        with patch("aplos_nca_saas_sdk.nca_resources.nca_analysis.requests.get",
                    return_value=_make_http_response()) as mock_get:
            result = analysis.execution_status(RESOURCE_ID)

        expected_url = f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/executions/{RESOURCE_ID}/status"
        mock_get.assert_called_once()
        actual_url = mock_get.call_args[0][0]
        assert actual_url == expected_url

    @patch(MOCK_AUTH)
    def test_execution_cancel_url(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_analysis import NCAAnalysis

        analysis = NCAAnalysis(HOST)
        analysis._NCAApiBaseClass__api_version = "v3"
        analysis._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        with patch("aplos_nca_saas_sdk.nca_resources.nca_analysis.requests.post",
                    return_value=_make_http_response()) as mock_post:
            analysis.execution_cancel(RESOURCE_ID)

        expected_url = f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/executions/{RESOURCE_ID}/cancel"
        assert mock_post.call_args[0][0] == expected_url

    @patch(MOCK_AUTH)
    def test_execution_output_by_type_url(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_analysis import NCAAnalysis

        analysis = NCAAnalysis(HOST)
        analysis._NCAApiBaseClass__api_version = "v3"
        analysis._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        with patch("aplos_nca_saas_sdk.nca_resources.nca_analysis.requests.get",
                    return_value=_make_http_response()) as mock_get:
            analysis.execution_output_by_type(RESOURCE_ID, "csv")

        expected_url = (
            f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}"
            f"/executions/{RESOURCE_ID}/outputs/type/csv"
        )
        assert mock_get.call_args[0][0] == expected_url


# ===================================================================
# NCAFileUpload tests
# ===================================================================

class TestNCAFileUploadV3Endpoints:
    """Test NCAFileUpload v3 methods produce correct endpoint URLs."""

    @patch(MOCK_AUTH)
    def test_file_archive_url(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_file_upload import NCAFileUpload

        upload = NCAFileUpload(HOST)
        upload._NCAApiBaseClass__api_version = "v3"
        upload._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        with patch("aplos_nca_saas_sdk.nca_resources.nca_file_upload.requests.post",
                    return_value=_make_http_response()) as mock_post:
            upload.file_archive(RESOURCE_ID)

        expected_url = f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/files/{RESOURCE_ID}/archive"
        assert mock_post.call_args[0][0] == expected_url

    @patch(MOCK_AUTH)
    def test_file_meta_url(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_file_upload import NCAFileUpload

        upload = NCAFileUpload(HOST)
        upload._NCAApiBaseClass__api_version = "v3"
        upload._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        with patch("aplos_nca_saas_sdk.nca_resources.nca_file_upload.requests.get",
                    return_value=_make_http_response()) as mock_get:
            upload.file_meta(RESOURCE_ID)

        expected_url = f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/files/{RESOURCE_ID}/meta"
        assert mock_get.call_args[0][0] == expected_url


# ===================================================================
# NCAFileDownload tests
# ===================================================================

class TestNCAFileDownloadV3Endpoints:
    """Test NCAFileDownload v3 methods produce correct endpoint URLs."""

    @patch(MOCK_AUTH)
    def test_file_download_url_endpoint(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_file_download import NCAFileDownload

        dl = NCAFileDownload(HOST)
        dl._NCAApiBaseClass__api_version = "v3"
        dl._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        with patch("aplos_nca_saas_sdk.nca_resources.nca_file_download.requests.get",
                    return_value=_make_http_response()) as mock_get:
            dl.file_download_url(RESOURCE_ID)

        expected_url = f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/files/{RESOURCE_ID}/download-url"
        assert mock_get.call_args[0][0] == expected_url

    @patch(MOCK_AUTH)
    def test_file_lineage_url(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_file_download import NCAFileDownload

        dl = NCAFileDownload(HOST)
        dl._NCAApiBaseClass__api_version = "v3"
        dl._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        with patch("aplos_nca_saas_sdk.nca_resources.nca_file_download.requests.get",
                    return_value=_make_http_response()) as mock_get:
            dl.file_lineage(RESOURCE_ID)

        expected_url = f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/files/{RESOURCE_ID}/lineage"
        assert mock_get.call_args[0][0] == expected_url


# ===================================================================
# NCAValidation tests
# ===================================================================

class TestNCAValidationV3Routing:
    """Test NCAValidation v3 routing."""

    @patch(MOCK_AUTH)
    def test_execute_uses_v3_validations_url(self, mock_auth_cls: MagicMock) -> None:
        """When api_version is v3, execute() should POST to the v3 validations endpoint."""
        mock_auth = _make_mock_auth()
        mock_auth_cls.return_value = mock_auth

        from aplos_nca_saas_sdk.nca_resources.nca_validations import NCAValidation

        val = NCAValidation(HOST)
        val._NCAApiBaseClass__api_version = "v3"
        val._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        # Mock the POST (queue) and GET (poll) calls
        post_resp = _make_http_response(json_data={
            "data": {"validation_batch": {"id": "batch-123"}},
            "statusCode": 200,
            "timestamp": "2025-01-01T00:00:00Z",
            "success": True,
            "diagnostics": {},
        })
        get_resp = _make_http_response(json_data={
            "data": {"status": "complete", "validation_batch": {"id": "batch-123"}},
            "statusCode": 200,
            "timestamp": "2025-01-01T00:00:00Z",
            "success": True,
            "diagnostics": {},
        })

        with patch("aplos_nca_saas_sdk.nca_resources.nca_validations.requests.post",
                    return_value=post_resp) as mock_post, \
             patch("aplos_nca_saas_sdk.nca_resources.nca_validations.requests.get",
                    return_value=get_resp):
            val.execute("user", "pass", wait_for_results=True)

        expected_url = f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/nca/validations"
        assert mock_post.call_args[0][0] == expected_url


# ===================================================================
# NCATenantUserManagement tests
# ===================================================================

class TestNCATenantUserManagementV3Endpoints:
    """Test tenant/user management operations produce correct endpoint URLs."""

    @patch(MOCK_AUTH)
    def test_get_tenant_url(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_tenant_user_management import (
            NCATenantUserManagement,
        )

        mgmt = NCATenantUserManagement(HOST)
        mgmt._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        with patch("aplos_nca_saas_sdk.nca_resources.nca_tenant_user_management.requests.get",
                    return_value=_make_http_response()) as mock_get:
            mgmt.get_tenant()

        expected_url = f"https://{HOST}/v3/tenants/{TENANT_ID}"
        assert mock_get.call_args[0][0] == expected_url

    @patch(MOCK_AUTH)
    def test_get_user_metrics_url(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_tenant_user_management import (
            NCATenantUserManagement,
        )

        mgmt = NCATenantUserManagement(HOST)
        mgmt._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        with patch("aplos_nca_saas_sdk.nca_resources.nca_tenant_user_management.requests.get",
                    return_value=_make_http_response()) as mock_get:
            mgmt.get_user_metrics()

        expected_url = f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/metrics"
        assert mock_get.call_args[0][0] == expected_url

    @patch(MOCK_AUTH)
    def test_get_assignable_roles_url(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_tenant_user_management import (
            NCATenantUserManagement,
        )

        mgmt = NCATenantUserManagement(HOST)
        mgmt._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        with patch("aplos_nca_saas_sdk.nca_resources.nca_tenant_user_management.requests.get",
                    return_value=_make_http_response()) as mock_get:
            mgmt.get_assignable_roles()

        expected_url = f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/assignable-roles"
        assert mock_get.call_args[0][0] == expected_url

    @patch(MOCK_AUTH)
    def test_get_public_messages_url(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_tenant_user_management import (
            NCATenantUserManagement,
        )

        mgmt = NCATenantUserManagement(HOST)
        mgmt._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        with patch("aplos_nca_saas_sdk.nca_resources.nca_tenant_user_management.requests.get",
                    return_value=_make_http_response()) as mock_get:
            mgmt.get_public_messages()

        expected_url = f"https://{HOST}/v3/app/messages"
        assert mock_get.call_args[0][0] == expected_url


# ===================================================================
# Backward compatibility tests (v1 defaults)
# ===================================================================

class TestResourceClassesV1BackwardCompat:
    """Test all resource classes still work with v1 defaults."""

    @patch(MOCK_AUTH)
    def test_nca_analysis_defaults_to_v1(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_analysis import NCAAnalysis

        analysis = NCAAnalysis(HOST)
        assert analysis.api_version == "v1"

    @patch(MOCK_AUTH)
    def test_nca_file_upload_defaults_to_v1(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_file_upload import NCAFileUpload

        upload = NCAFileUpload(HOST)
        assert upload.api_version == "v1"

    @patch(MOCK_AUTH)
    def test_nca_file_download_defaults_to_v1(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_file_download import NCAFileDownload

        dl = NCAFileDownload(HOST)
        assert dl.api_version == "v1"

    @patch(MOCK_AUTH)
    def test_nca_validation_defaults_to_v1(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_validations import NCAValidation

        val = NCAValidation(HOST)
        assert val.api_version == "v1"

    @patch(MOCK_AUTH)
    def test_nca_tenant_user_mgmt_defaults_to_v1(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_tenant_user_management import (
            NCATenantUserManagement,
        )

        mgmt = NCATenantUserManagement(HOST)
        assert mgmt.api_version == "v1"


# ===================================================================
# V3 diagnostic envelope unwrapping tests
# ===================================================================

class TestV3ResponseEnvelopeUnwrapping:
    """Test v3 responses are unwrapped through diagnostic envelope handler."""

    @patch(MOCK_AUTH)
    def test_analysis_execution_status_unwraps_envelope(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_analysis import NCAAnalysis

        analysis = NCAAnalysis(HOST)
        analysis._NCAApiBaseClass__api_version = "v3"
        analysis._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        with patch("aplos_nca_saas_sdk.nca_resources.nca_analysis.requests.get",
                    return_value=_make_http_response()):
            result = analysis.execution_status(RESOURCE_ID)

        assert result == UNWRAPPED
        assert "_diagnostics" in result

    @patch(MOCK_AUTH)
    def test_file_download_url_unwraps_envelope(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_file_download import NCAFileDownload

        dl = NCAFileDownload(HOST)
        dl._NCAApiBaseClass__api_version = "v3"
        dl._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        with patch("aplos_nca_saas_sdk.nca_resources.nca_file_download.requests.get",
                    return_value=_make_http_response()):
            result = dl.file_download_url(RESOURCE_ID)

        assert result == UNWRAPPED
        assert "_diagnostics" in result

    @patch(MOCK_AUTH)
    def test_tenant_mgmt_get_tenant_unwraps_envelope(self, mock_auth_cls: MagicMock) -> None:
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_tenant_user_management import (
            NCATenantUserManagement,
        )

        mgmt = NCATenantUserManagement(HOST)
        mgmt._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        with patch("aplos_nca_saas_sdk.nca_resources.nca_tenant_user_management.requests.get",
                    return_value=_make_http_response()):
            result = mgmt.get_tenant()

        assert result == UNWRAPPED
        assert "_diagnostics" in result

    @patch(MOCK_AUTH)
    def test_non_envelope_response_passes_through(self, mock_auth_cls: MagicMock) -> None:
        """A v3 response that is NOT an envelope should pass through unchanged."""
        mock_auth_cls.return_value = _make_mock_auth()
        from aplos_nca_saas_sdk.nca_resources.nca_analysis import NCAAnalysis

        analysis = NCAAnalysis(HOST)
        analysis._NCAApiBaseClass__api_version = "v3"
        analysis._NCAApiBaseClass__router = _mock_router(_make_v3_strategy())

        non_envelope = {"status": "complete", "execution_id": "abc"}
        with patch("aplos_nca_saas_sdk.nca_resources.nca_analysis.requests.get",
                    return_value=_make_http_response(json_data=non_envelope)):
            result = analysis.execution_status(RESOURCE_ID)

        assert result == non_envelope
