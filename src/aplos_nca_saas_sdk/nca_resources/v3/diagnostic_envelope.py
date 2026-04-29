"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from dataclasses import dataclass
from typing import Any

ENVELOPE_KEYS: set[str] = {"data", "statusCode", "timestamp", "success", "diagnostics"}


@dataclass
class DiagnosticEnvelope:
    """Represents a v3 API diagnostic response envelope."""

    data: dict[str, Any]
    status_code: int
    timestamp: str
    success: bool
    diagnostics: dict[str, Any]  # contains startTime, endTime, duration

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "DiagnosticEnvelope":
        """Deserialize a raw response dict into a DiagnosticEnvelope."""
        return cls(
            data=d["data"],
            status_code=d["statusCode"],
            timestamp=d["timestamp"],
            success=d["success"],
            diagnostics=d.get("diagnostics", {}),
        )


class DiagnosticEnvelopeHandler:
    """Handles v3 diagnostic response envelope detection and unwrapping."""

    @staticmethod
    def is_envelope(response: dict[str, Any]) -> bool:
        """Detect if a response dict matches the diagnostic envelope structure."""
        if not isinstance(response, dict):
            return False
        return ENVELOPE_KEYS.issubset(response.keys())

    @staticmethod
    def unwrap(response: dict[str, Any]) -> dict[str, Any]:
        """Unwrap a diagnostic envelope, returning the inner data.

        Non-envelope responses pass through unchanged.
        """
        if DiagnosticEnvelopeHandler.is_envelope(response):
            data = response["data"]
            result = data if isinstance(data, dict) else {"_value": data}
            result["_diagnostics"] = response.get("diagnostics", {})
            return result
        return response

    @staticmethod
    def get_diagnostics(response: dict[str, Any]) -> dict[str, Any] | None:
        """Extract diagnostics metadata from an envelope response."""
        if DiagnosticEnvelopeHandler.is_envelope(response):
            return response.get("diagnostics")
        return None
