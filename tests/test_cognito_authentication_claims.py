"""
CognitoAuthentication reads the authenticated user/tenant ids from the NEW JWT
claims first (``custom:user_id`` / ``custom:tenant_id``), falling back to the
retired ``custom:aplos_*`` claims only for environments that have not been
upgraded yet.

Before this fix the SDK read ONLY the retired claims, so any account whose
Cognito attributes were new-only (every account saved/created after the claim
migration) logged in fine but then raised ``RuntimeError("Failed to get a user
id")`` on first use, breaking every call that builds
``/tenants/{tenant-id}/users/{user-id}/...``.

The tests drive the real ``login()`` -> JWT parse path. Only the boto3 Cognito
client is replaced with a small hand-written fake that returns a signed JWT.
"""

import jwt as jwt_lib
import pytest

from aplos_nca_saas_sdk.nca_resources.aws_cognito import CognitoAuthentication


class _FakeCognitoClient:
    """Minimal stand-in for the boto3 cognito-idp client (login flow only)."""

    def __init__(self, claims: dict):
        self._claims = claims

    def initiate_auth(self, **_kwargs):
        id_token = jwt_lib.encode(self._claims, "test-secret", algorithm="HS256")
        return {
            "AuthenticationResult": {
                "IdToken": id_token,
                "AccessToken": "access-token",
                "RefreshToken": "refresh-token",
            }
        }


def _login(monkeypatch, claims: dict) -> CognitoAuthentication:
    monkeypatch.setattr(
        "aplos_nca_saas_sdk.nca_resources.aws_cognito.boto3.client",
        lambda *_a, **_k: _FakeCognitoClient(claims),
    )
    auth = CognitoAuthentication(client_id="client-123", region="us-east-1")
    auth.login("user@example.com", "password")
    return auth


class TestNewClaimsResolve:
    def test_new_only_token_resolves_user_and_tenant(self, monkeypatch):
        """The regression: a new-only token must not leave the ids unset."""
        auth = _login(
            monkeypatch,
            {"custom:user_id": "new-user", "custom:tenant_id": "new-tenant"},
        )

        assert auth.user_id == "new-user"
        assert auth.tenant_id == "new-tenant"

    def test_new_claims_win_when_both_sets_present(self, monkeypatch):
        auth = _login(
            monkeypatch,
            {
                "custom:user_id": "new-user",
                "custom:tenant_id": "new-tenant",
                "custom:aplos_user_id": "legacy-user",
                "custom:aplos_user_tenant_id": "legacy-tenant",
            },
        )

        assert auth.user_id == "new-user"
        assert auth.tenant_id == "new-tenant"


class TestRetiredFallback:
    def test_retired_only_token_still_resolves_for_not_yet_upgraded_environments(
        self, monkeypatch
    ):
        auth = _login(
            monkeypatch,
            {
                "custom:aplos_user_id": "legacy-user",
                "custom:aplos_user_tenant_id": "legacy-tenant",
            },
        )

        assert auth.user_id == "legacy-user"
        assert auth.tenant_id == "legacy-tenant"

    def test_each_id_falls_back_independently(self, monkeypatch):
        """A token can carry the new user id but only the retired tenant id."""
        auth = _login(
            monkeypatch,
            {
                "custom:user_id": "new-user",
                "custom:aplos_user_tenant_id": "legacy-tenant",
            },
        )

        assert auth.user_id == "new-user"
        assert auth.tenant_id == "legacy-tenant"


class TestNoIdentityClaims:
    def test_token_with_no_identity_claims_fails_loudly(self, monkeypatch):
        """No silent failure: asking for the ids raises a clear error."""
        auth = _login(monkeypatch, {"email": "user@example.com"})

        with pytest.raises(RuntimeError, match="Failed to get a user id"):
            _ = auth.user_id
        with pytest.raises(RuntimeError, match="Failed to get a tenant id"):
            _ = auth.tenant_id
