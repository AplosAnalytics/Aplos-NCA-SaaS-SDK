"""
Unit tests for DiagnosticEnvelopeHandler and V3EndpointStrategy.

Tests cover:
- is_envelope() returns True for valid envelopes, False for partial/missing keys
- unwrap() extracts data and attaches diagnostics
- unwrap() passthrough for non-envelope responses
- Each v3 operation produces the correct URL
- process_response() delegates to envelope handler

Requirements: 2.2, 2.4, 5.1, 5.2, 5.3, 5.4, 5.5
"""

from typing import Any

from aplos_nca_saas_sdk.nca_resources.v3.diagnostic_envelope import (
    DiagnosticEnvelopeHandler,
    ENVELOPE_KEYS,
)
from aplos_nca_saas_sdk.nca_resources.v3.endpoint_strategy import V3EndpointStrategy

HOST = "api.example.com"
TENANT_ID = "aaaa-bbbb-cccc-dddd"
USER_ID = "1111-2222-3333-4444"
RESOURCE_ID = "rrrr-ssss-tttt-uuuu"
SUB_RESOURCE = "plots"


def _make_envelope(
    data: dict[str, Any] | None = None,
    diagnostics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Helper to build a valid diagnostic envelope."""
    return {
        "data": data or {"result": "ok"},
        "statusCode": 200,
        "timestamp": "2025-01-15T12:00:00Z",
        "success": True,
        "diagnostics": diagnostics or {
            "startTime": "2025-01-15T12:00:00Z",
            "endTime": "2025-01-15T12:00:01Z",
            "duration": 1000,
        },
    }


# ---------------------------------------------------------------------------
# DiagnosticEnvelopeHandler.is_envelope()
# ---------------------------------------------------------------------------

class TestIsEnvelope:
    """Tests for is_envelope() detection."""

    def test_valid_envelope_returns_true(self) -> None:
        envelope = _make_envelope()
        assert DiagnosticEnvelopeHandler.is_envelope(envelope) is True

    def test_envelope_with_extra_keys_returns_true(self) -> None:
        envelope = _make_envelope()
        envelope["extra"] = "field"
        assert DiagnosticEnvelopeHandler.is_envelope(envelope) is True

    def test_missing_data_key_returns_false(self) -> None:
        envelope = _make_envelope()
        del envelope["data"]
        assert DiagnosticEnvelopeHandler.is_envelope(envelope) is False

    def test_missing_statusCode_returns_false(self) -> None:
        envelope = _make_envelope()
        del envelope["statusCode"]
        assert DiagnosticEnvelopeHandler.is_envelope(envelope) is False

    def test_missing_timestamp_returns_false(self) -> None:
        envelope = _make_envelope()
        del envelope["timestamp"]
        assert DiagnosticEnvelopeHandler.is_envelope(envelope) is False

    def test_missing_success_returns_false(self) -> None:
        envelope = _make_envelope()
        del envelope["success"]
        assert DiagnosticEnvelopeHandler.is_envelope(envelope) is False

    def test_missing_diagnostics_returns_false(self) -> None:
        envelope = _make_envelope()
        del envelope["diagnostics"]
        assert DiagnosticEnvelopeHandler.is_envelope(envelope) is False

    def test_empty_dict_returns_false(self) -> None:
        assert DiagnosticEnvelopeHandler.is_envelope({}) is False

    def test_non_dict_returns_false(self) -> None:
        assert DiagnosticEnvelopeHandler.is_envelope("not a dict") is False  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# DiagnosticEnvelopeHandler.unwrap()
# ---------------------------------------------------------------------------

class TestUnwrap:
    """Tests for unwrap() extraction and passthrough."""

    def test_unwrap_extracts_data(self) -> None:
        data = {"name": "test", "value": 42}
        envelope = _make_envelope(data=data)
        result = DiagnosticEnvelopeHandler.unwrap(envelope)
        assert result["name"] == "test"
        assert result["value"] == 42

    def test_unwrap_attaches_diagnostics(self) -> None:
        diagnostics = {"startTime": "t0", "endTime": "t1", "duration": 500}
        envelope = _make_envelope(diagnostics=diagnostics)
        result = DiagnosticEnvelopeHandler.unwrap(envelope)
        assert "_diagnostics" in result
        assert result["_diagnostics"] == diagnostics

    def test_unwrap_non_dict_data_wraps_in_value_key(self) -> None:
        envelope = _make_envelope()
        envelope["data"] = "scalar_value"
        result = DiagnosticEnvelopeHandler.unwrap(envelope)
        assert result["_value"] == "scalar_value"
        assert "_diagnostics" in result

    def test_unwrap_passthrough_for_non_envelope(self) -> None:
        response: dict[str, Any] = {"key": "value", "count": 10}
        result = DiagnosticEnvelopeHandler.unwrap(response)
        assert result is response

    def test_unwrap_passthrough_for_empty_dict(self) -> None:
        response: dict[str, Any] = {}
        result = DiagnosticEnvelopeHandler.unwrap(response)
        assert result is response

    def test_unwrap_passthrough_for_partial_envelope(self) -> None:
        partial = {"data": {"x": 1}, "statusCode": 200}
        result = DiagnosticEnvelopeHandler.unwrap(partial)
        assert result is partial


# ---------------------------------------------------------------------------
# V3EndpointStrategy URL construction
# ---------------------------------------------------------------------------

class TestV3EndpointStrategyVersion:
    """Tests for the version property."""

    def test_version_returns_v3(self) -> None:
        strategy = V3EndpointStrategy()
        assert strategy.version == "v3"


class TestV3EndpointStrategyURLs:
    """Tests for get_endpoint_url with known IDs."""

    def setup_method(self) -> None:
        self.strategy = V3EndpointStrategy()

    def test_app_configuration(self) -> None:
        url = self.strategy.get_endpoint_url("app_configuration", host=HOST)
        assert url == f"https://{HOST}/v3/app/configuration"

    def test_tenant(self) -> None:
        url = self.strategy.get_endpoint_url("tenant", host=HOST, tenant_id=TENANT_ID)
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}"

    def test_user(self) -> None:
        url = self.strategy.get_endpoint_url(
            "user", host=HOST, tenant_id=TENANT_ID, user_id=USER_ID
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}"

    def test_executions(self) -> None:
        url = self.strategy.get_endpoint_url(
            "executions", host=HOST, tenant_id=TENANT_ID, user_id=USER_ID
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/nca/executions"

    def test_execution(self) -> None:
        url = self.strategy.get_endpoint_url(
            "execution", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/nca/executions/{RESOURCE_ID}"

    def test_analysis_queue(self) -> None:
        url = self.strategy.get_endpoint_url(
            "analysis_queue", host=HOST, tenant_id=TENANT_ID, user_id=USER_ID
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/analysis/queue"

    def test_execution_status(self) -> None:
        url = self.strategy.get_endpoint_url(
            "execution_status", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/executions/{RESOURCE_ID}/status"

    def test_execution_cancel(self) -> None:
        url = self.strategy.get_endpoint_url(
            "execution_cancel", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/executions/{RESOURCE_ID}/cancel"

    def test_execution_archive(self) -> None:
        url = self.strategy.get_endpoint_url(
            "execution_archive", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/executions/{RESOURCE_ID}/archive"

    def test_execution_output_by_type(self) -> None:
        url = self.strategy.get_endpoint_url(
            "execution_output_by_type", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID, sub_resource=SUB_RESOURCE,
        )
        assert url == (
            f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}"
            f"/executions/{RESOURCE_ID}/outputs/type/{SUB_RESOURCE}"
        )

    def test_files(self) -> None:
        url = self.strategy.get_endpoint_url(
            "files", host=HOST, tenant_id=TENANT_ID, user_id=USER_ID
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/files"

    def test_file(self) -> None:
        url = self.strategy.get_endpoint_url(
            "file", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/files/{RESOURCE_ID}"

    def test_file_download_url(self) -> None:
        url = self.strategy.get_endpoint_url(
            "file_download_url", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/files/{RESOURCE_ID}/download-url"

    def test_file_stream(self) -> None:
        url = self.strategy.get_endpoint_url(
            "file_stream", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/files/{RESOURCE_ID}/stream"

    def test_file_lineage(self) -> None:
        url = self.strategy.get_endpoint_url(
            "file_lineage", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/files/{RESOURCE_ID}/lineage"

    def test_file_meta(self) -> None:
        url = self.strategy.get_endpoint_url(
            "file_meta", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/files/{RESOURCE_ID}/meta"

    def test_file_archive(self) -> None:
        url = self.strategy.get_endpoint_url(
            "file_archive", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/files/{RESOURCE_ID}/archive"

    def test_file_unarchive(self) -> None:
        url = self.strategy.get_endpoint_url(
            "file_unarchive", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/files/{RESOURCE_ID}/unarchive"

    def test_tenant_subscriptions(self) -> None:
        url = self.strategy.get_endpoint_url(
            "tenant_subscriptions", host=HOST, tenant_id=TENANT_ID
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/subscriptions"

    def test_update_subscription(self) -> None:
        url = self.strategy.get_endpoint_url(
            "update_subscription", host=HOST, tenant_id=TENANT_ID,
            resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/subscriptions/{RESOURCE_ID}"

    def test_user_metrics(self) -> None:
        url = self.strategy.get_endpoint_url(
            "user_metrics", host=HOST, tenant_id=TENANT_ID, user_id=USER_ID
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/metrics"

    def test_tenant_metrics(self) -> None:
        url = self.strategy.get_endpoint_url(
            "tenant_metrics", host=HOST, tenant_id=TENANT_ID
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/metrics"

    def test_public_messages(self) -> None:
        url = self.strategy.get_endpoint_url("public_messages", host=HOST)
        assert url == f"https://{HOST}/v3/app/messages"

    def test_user_messages(self) -> None:
        url = self.strategy.get_endpoint_url(
            "user_messages", host=HOST, tenant_id=TENANT_ID, user_id=USER_ID
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/messages"

    def test_company_logos(self) -> None:
        url = self.strategy.get_endpoint_url("company_logos", host=HOST)
        assert url == f"https://{HOST}/v3/app/company-logos"

    def test_assignable_roles(self) -> None:
        url = self.strategy.get_endpoint_url(
            "assignable_roles", host=HOST, tenant_id=TENANT_ID, user_id=USER_ID
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/assignable-roles"

    def test_validations(self) -> None:
        url = self.strategy.get_endpoint_url(
            "validations", host=HOST, tenant_id=TENANT_ID, user_id=USER_ID
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/nca/validations"

    def test_validation(self) -> None:
        url = self.strategy.get_endpoint_url(
            "validation", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/nca/validations/{RESOURCE_ID}"

    def test_execution_config(self) -> None:
        url = self.strategy.get_endpoint_url(
            "execution_config", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/executions/{RESOURCE_ID}/config"

    def test_execution_outputs_package(self) -> None:
        url = self.strategy.get_endpoint_url(
            "execution_outputs_package", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/executions/{RESOURCE_ID}/outputs/package"

    def test_execution_outputs_report(self) -> None:
        url = self.strategy.get_endpoint_url(
            "execution_outputs_report", host=HOST, tenant_id=TENANT_ID,
            user_id=USER_ID, resource_id=RESOURCE_ID,
        )
        assert url == f"https://{HOST}/v3/tenants/{TENANT_ID}/users/{USER_ID}/executions/{RESOURCE_ID}/outputs/report"



# ---------------------------------------------------------------------------
# V3EndpointStrategy.process_response()
# ---------------------------------------------------------------------------

class TestV3ProcessResponse:
    """Tests for process_response() delegation to envelope handler."""

    def test_process_response_unwraps_envelope(self) -> None:
        strategy = V3EndpointStrategy()
        data = {"result": "success"}
        diagnostics = {"duration": 100}
        envelope = _make_envelope(data=data, diagnostics=diagnostics)
        result = strategy.process_response(envelope)
        assert result["result"] == "success"
        assert result["_diagnostics"] == diagnostics

    def test_process_response_passthrough_non_envelope(self) -> None:
        strategy = V3EndpointStrategy()
        response: dict[str, Any] = {"plain": "response"}
        result = strategy.process_response(response)
        assert result is response
