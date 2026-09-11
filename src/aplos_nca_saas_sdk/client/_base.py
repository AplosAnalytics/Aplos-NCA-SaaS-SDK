"""Shared plumbing for the AplosClient facade.

The facade wraps the generated (transport) client with:
- Cognito auth bootstrap -> AuthenticatedClient(token=...)
- envelope unwrapping (return the typed `data`, raise AplosApiError on error)
- session-scoped tenant_id / user_id auto-fill

See NE-1849-codegen-design.md.
"""

from __future__ import annotations

from typing import Any, Callable, TypeVar

from aplos_nca_saas_sdk._generated import errors as _gen_errors
from aplos_nca_saas_sdk._generated.client import AuthenticatedClient
from aplos_nca_saas_sdk._generated.models.error_envelope import ErrorEnvelope
from aplos_nca_saas_sdk._generated.types import UNSET
from aplos_nca_saas_sdk.client.errors import AplosApiError

T = TypeVar("T")


def unwrap(result: Any) -> Any:
    """Convert a generated operation result into an ergonomic value.

    - If the result is an ``ErrorEnvelope``, raise ``AplosApiError``.
    - If the result is a success wrapper with a ``data`` attribute, return
      ``data`` (the typed entity or the list/pagination payload).
    - Otherwise return the result as-is (e.g. 204 -> None).
    """
    if result is None:
        return None

    if isinstance(result, ErrorEnvelope):
        err = result.error
        message = getattr(err, "message", None) or "API error"
        code = getattr(err, "code", None)
        details = getattr(err, "details", None)
        status = getattr(result, "status_code", None)
        raise AplosApiError(
            message=message, code=code, status_code=status, details=details
        )

    # Success envelope wrappers expose a `data` attribute.
    if hasattr(result, "data"):
        data = result.data
        return None if data is UNSET else data

    return result


class _DomainClient:
    """Base for domain namespaces (client.users, client.workflow, ...).

    Holds a reference back to the owning AplosClient so domain methods can
    reach the transport client and the session tenant/user ids.
    """

    def __init__(self, root: "AplosClientProtocol") -> None:
        self._root = root

    @property
    def _client(self) -> AuthenticatedClient:
        return self._root.transport

    @property
    def _tenant_id(self) -> str:
        return self._root.tenant_id

    @property
    def _user_id(self) -> str:
        return self._root.user_id

    def _call(self, op_sync: Callable[..., Any], /, **kwargs: Any) -> Any:
        """Invoke a generated ``sync`` operation and unwrap the result.

        ``op_sync`` is a generated module's ``sync`` function. The transport
        client is injected automatically; caller supplies path/query/body args.
        """
        try:
            result = op_sync(client=self._client, **kwargs)
        except _gen_errors.UnexpectedStatus as exc:  # pragma: no cover - passthrough
            raise AplosApiError(
                message=f"Unexpected API status: {exc.status_code}",
                status_code=exc.status_code,
            ) from exc
        return unwrap(result)


class AplosClientProtocol:
    """Structural type the domain clients rely on (avoids a hard import cycle)."""

    transport: AuthenticatedClient
    tenant_id: str
    user_id: str
