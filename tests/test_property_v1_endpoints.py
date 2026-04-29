"""
Property 2: V1 endpoint URL construction invariant

For any valid operation name, tenant_id, and user_id, the URL produced by
V1EndpointStrategy.get_endpoint_url() SHALL NOT contain a version prefix
segment (no /v1/, /v3/, etc.) and SHALL match the pattern
https://{host}/tenants/{tenant_id}/users/{user_id}/... or
https://{host}/app/... consistent with the current NCAEndpoints class behavior.

**Validates: Requirements 2.1, 2.3**
Tag: Feature: sdk-v3-api-upgrade, Property 2: V1 endpoint URL construction invariant
"""

import re
from urllib.parse import urlparse

from hypothesis import given, settings
from hypothesis import strategies as st

from aplos_nca_saas_sdk.nca_resources.v1.endpoint_strategy import V1EndpointStrategy

# Fixed host for URL construction
HOST = "api.example.com"

# UUID strategy for tenant_id, user_id, resource_id
uuid_st = st.uuids().map(str)


@given(tenant_id=uuid_st, user_id=uuid_st, resource_id=uuid_st, sub_resource=st.text(min_size=1, max_size=20))
@settings(max_examples=100)
def test_v1_urls_have_no_version_prefix(
    tenant_id: str, user_id: str, resource_id: str, sub_resource: str
) -> None:
    """Property 2: V1 endpoint URL construction invariant

    **Validates: Requirements 2.1, 2.3**

    For every operation in V1EndpointStrategy.OPERATIONS, the constructed URL
    must NOT contain /v1/ or /v3/ as a path prefix segment, and must match
    either https://{host}/tenants/... or https://{host}/app/... pattern.
    """
    strategy = V1EndpointStrategy()

    for operation in V1EndpointStrategy.OPERATIONS:
        url = strategy.get_endpoint_url(
            operation,
            host=HOST,
            tenant_id=tenant_id,
            user_id=user_id,
            resource_id=resource_id,
            sub_resource=sub_resource,
        )

        parsed = urlparse(url)
        path = parsed.path

        # No version prefix segments in the path
        assert not re.search(r"/v\d+/", path), (
            f"Operation '{operation}' URL contains a version prefix: {path}"
        )

        # URL must start with https://{host}
        assert url.startswith(f"https://{HOST}"), (
            f"Operation '{operation}' URL does not start with https://{HOST}: {url}"
        )

        # Path must match /tenants/... or /app/... pattern
        assert path.startswith("/tenants/") or path.startswith("/app/"), (
            f"Operation '{operation}' URL path does not match expected pattern: {path}"
        )
