"""AplosClient — the public, ergonomic entry point for the Aplos NCA SaaS SDK.

Wraps the generated typed transport client with:
- Cognito username/password auth (reusing the existing NCAAuthenticator), or a
  pre-obtained bearer token;
- typed, domain-grouped operations (``client.users``, ``client.workflow``, ...);
- envelope unwrapping (returns the typed ``data``, raises ``AplosApiError``).

Example:
    from aplos_nca_saas_sdk.client import AplosClient

    client = AplosClient(host="api.dev.aplos-nca.com")
    client.login(username="me@example.com", password="...")

    user = client.users.get(client.user_id)          # typed User
    history = client.workflow.history()               # pagination payload
    status = client.workflow.status("exec-123")       # typed Execution

The generated transport lives in ``aplos_nca_saas_sdk._generated`` and is never
hand-edited; see NE-1849-codegen-design.md.
"""

from __future__ import annotations

from typing import Optional

from aplos_nca_saas_sdk._generated.client import AuthenticatedClient
from aplos_nca_saas_sdk.client.domains import (
    SubscriptionsClient,
    TenantsClient,
    UsersClient,
    WorkflowClient,
)
from aplos_nca_saas_sdk.nca_resources.nca_authenticator import NCAAuthenticator


class AplosClient:
    """Public facade over the generated v3 API client."""

    def __init__(
        self,
        host: str,
        *,
        token: Optional[str] = None,
        tenant_id: Optional[str] = None,
        user_id: Optional[str] = None,
        base_url: Optional[str] = None,
        verify_ssl: bool = True,
        timeout: Optional[float] = None,
    ) -> None:
        """Create a client.

        Args:
            host: The Aplos host (e.g. "api.dev.aplos-nca.com"). Used to build
                the API base URL and to auto-discover Cognito settings on login.
            token: Optional pre-obtained Cognito JWT. If given, the client is
                ready to use without calling ``login()`` (supply tenant_id /
                user_id too, or they can be provided per-call).
            tenant_id: Session tenant id (auto-set on ``login()``).
            user_id: Session user id (auto-set on ``login()``).
            base_url: Override the API base URL. Defaults to
                ``https://{host}/api``.
            verify_ssl: Verify TLS certs (True in production).
            timeout: Per-request timeout in seconds.
        """
        self._host = host
        self._base_url = base_url or f"https://{host}/api"
        self._verify_ssl = verify_ssl
        self._timeout = timeout

        self._authenticator = NCAAuthenticator(host=host)
        self._token: Optional[str] = token
        self._tenant_id: Optional[str] = tenant_id
        self._user_id: Optional[str] = user_id
        self._transport: Optional[AuthenticatedClient] = None

        if token is not None:
            self._build_transport()

        # Domain namespaces.
        self.users = UsersClient(self)  # type: ignore[arg-type]
        self.tenants = TenantsClient(self)  # type: ignore[arg-type]
        self.subscriptions = SubscriptionsClient(self)  # type: ignore[arg-type]
        self.workflow = WorkflowClient(self)  # type: ignore[arg-type]

    # ------------------------------------------------------------------ auth

    def login(self, username: str, password: str) -> "AplosClient":
        """Authenticate via Cognito and prepare the transport client.

        Populates the bearer token plus session ``tenant_id`` / ``user_id``
        from the resulting Cognito session.
        """
        self._token = self._authenticator.authenticate(username, password)
        cognito = self._authenticator.cognito
        self._tenant_id = self._tenant_id or cognito.tenant_id
        self._user_id = self._user_id or cognito.user_id
        self._build_transport()
        return self

    def _build_transport(self) -> None:
        if not self._token:
            raise RuntimeError("Cannot build transport without a token; call login().")
        kwargs = {"base_url": self._base_url, "token": self._token,
                  "verify_ssl": self._verify_ssl}
        transport = AuthenticatedClient(**kwargs)  # type: ignore[arg-type]
        if self._timeout is not None:
            import httpx

            transport = transport.with_timeout(httpx.Timeout(self._timeout))
        self._transport = transport

    # -------------------------------------------------------------- accessors

    @property
    def transport(self) -> AuthenticatedClient:
        """The underlying generated AuthenticatedClient (transport layer)."""
        if self._transport is None:
            raise RuntimeError(
                "Client is not authenticated. Call login(username, password) "
                "or construct AplosClient(..., token=...)."
            )
        return self._transport

    @property
    def tenant_id(self) -> str:
        if not self._tenant_id:
            raise RuntimeError(
                "No tenant_id in session. Call login() or pass tenant_id."
            )
        return self._tenant_id

    @property
    def user_id(self) -> str:
        if not self._user_id:
            raise RuntimeError("No user_id in session. Call login() or pass user_id.")
        return self._user_id

    @property
    def host(self) -> str:
        return self._host
