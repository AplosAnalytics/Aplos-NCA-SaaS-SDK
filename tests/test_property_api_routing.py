"""
Property test for ApiRoutingConfig.from_dict().

Property 6: API routing configuration parsing

Tag: Feature: sdk-v3-api-upgrade, Property 6: API routing configuration parsing
"""

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from aplos_nca_saas_sdk.nca_resources.v3.endpoint_strategy import ApiRoutingConfig

DOMAINS = ["users", "tenants", "subscriptions", "site_messages", "metrics"]

# Strategy for version strings like "v1", "v3", "v42", etc.
version_strings = st.from_regex(r"v[0-9]{1,3}", fullmatch=True)

# Strategy for non-dict values that might appear as domain values
non_dict_values = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-1000, max_value=1000),
    st.text(min_size=0, max_size=20),
    st.lists(st.integers(), max_size=3),
)

# Strategy for a single domain entry: either a dict with {"version": "vN"} or a non-dict
domain_entry = st.one_of(
    st.fixed_dictionaries({"version": version_strings}),
    non_dict_values,
)


@st.composite
def api_routing_dicts(draw: st.DrawFn) -> dict:
    """Generate api_routing dicts where each domain may or may not be present.

    When present, the value is either {"version": "vN"} or a non-dict value.
    """
    result: dict = {}
    for domain in DOMAINS:
        include = draw(st.booleans())
        if include:
            result[domain] = draw(domain_entry)
    return result


@given(routing=api_routing_dicts())
@settings(max_examples=200)
def test_api_routing_config_parsing(routing: dict) -> None:
    """Property 6: API routing configuration parsing

    **Validates: Requirements 11.2**

    For any api_routing dict with varying domain presence/absence,
    ApiRoutingConfig.from_dict() must:
    - Return "v3" for domains that are absent from the dict
    - Return "v3" for domains whose value is not a dict
    - Return the correct version string for domains with {"version": "vN"}
    """
    config = ApiRoutingConfig.from_dict(routing)

    for domain in DOMAINS:
        actual = getattr(config, domain)
        raw = routing.get(domain)

        if domain not in routing:
            # Missing domain → default "v3"
            assert actual == "v3", (
                f"Domain '{domain}' absent from routing but got '{actual}' instead of 'v3'"
            )
        elif not isinstance(raw, dict):
            # Non-dict value → default "v3"
            assert actual == "v3", (
                f"Domain '{domain}' has non-dict value {raw!r} but got '{actual}' instead of 'v3'"
            )
        else:
            # Dict value → extract version with "v3" fallback
            expected = raw.get("version", "v3")
            assert actual == expected, (
                f"Domain '{domain}' has dict {raw!r} but got '{actual}' instead of '{expected}'"
            )
