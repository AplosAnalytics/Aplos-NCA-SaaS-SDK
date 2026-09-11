"""Public, typed, ergonomic client for the Aplos NCA SaaS API (v3).

This is the recommended entry point. It wraps the generated transport client
(``aplos_nca_saas_sdk._generated``) with Cognito auth, envelope unwrapping, and
domain-grouped typed operations.

    from aplos_nca_saas_sdk.client import AplosClient

The older ``nca_resources`` classes remain available for backward compatibility
but are superseded by ``AplosClient``.
"""

from aplos_nca_saas_sdk.client.aplos_client import AplosClient
from aplos_nca_saas_sdk.client.errors import AplosApiError

__all__ = ["AplosClient", "AplosApiError"]
