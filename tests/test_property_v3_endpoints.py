"""
Property 3: V3 endpoint URL construction with domain routing

For any valid v3 operation name, tenant_id, user_id, and resource_id,
the URL produced by V3EndpointStrategy.get_endpoint_url() SHALL contain
the /v3/ version prefix and SHALL follow the correct path template for
that operation as defined in the v3 OPERATIONS registry.

**Validates: Requirements 2.2, 2.4, 2.5**
Tag: Feature: sdk-v3-api-upgrade, Property 3: V3 endpoint URL construction with domain routing
"""

from urllib.parse import urlparse

from hypothesis import given, settings
from hypothesis import strategies as st

from aplos_nca_saas_sdk.nca_resources.v3.endpoint_strategy import V3EndpointStrategy

HOST = "api.example.com"

uuid_st = st.uuids().map(str)


@given(
    tenant_id=uuid_st,
    user_id=uuid_st,
    resource_id=uuid_st,
    sub_resource=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_"),
        min_size=1,
        max_size=20,
    ),
)
@settings(max_examples=100)
def test_v3_urls_contain_v3_prefix_and_match_template(
    tenant_id: str, user_id: str, resource_id: str, sub_resource: str
) -> None:
    """Property 3: V3 endpoint URL construction with domain routing

    **Validates: Requirements 2.2, 2.4, 2.5**

    For every operation in V3EndpointStrategy.OPERATIONS, the constructed URL
    must contain /v3/ as a path prefix and must match the expected path
    template with the provided IDs substituted in.
    """
    strategy = V3EndpointStrategy()

    for operation, template in V3EndpointStrategy.OPERATIONS.items():
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

        # URL must contain /v3/ prefix
        assert "/v3/" in path, (
            f"Operation '{operation}' URL path missing /v3/ prefix: {path}"
        )

        # URL must start with https://{host}
        assert url.startswith(f"https://{HOST}"), (
            f"Operation '{operation}' URL does not start with https://{HOST}: {url}"
        )

        # The path must match the template with IDs substituted
        expected_path = template.format(
            tenant_id=tenant_id,
            user_id=user_id,
            resource_id=resource_id,
            sub_resource=sub_resource,
        )
        assert path == expected_path, (
            f"Operation '{operation}' URL path mismatch: "
            f"expected {expected_path!r}, got {path!r}"
        )
