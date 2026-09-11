"""Public exception types for the AplosClient facade."""

from __future__ import annotations

from typing import Any, Optional


class AplosApiError(RuntimeError):
    """Raised when the API returns an error envelope (non-2xx).

    Attributes:
        message: Human-readable error message from the API.
        code: The API error code (e.g. "VALIDATION_ERROR", "NOT_FOUND").
        status_code: HTTP status code, when known.
        details: Optional structured error details from the envelope.
    """

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        status_code: Optional[int] = None,
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details

    def __str__(self) -> str:
        parts = [self.message or "API error"]
        if self.code:
            parts.append(f"(code={self.code})")
        if self.status_code:
            parts.append(f"[HTTP {self.status_code}]")
        return " ".join(parts)
