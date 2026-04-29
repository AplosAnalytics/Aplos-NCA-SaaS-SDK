"""
Property tests for DiagnosticEnvelopeHandler.

Property 4: Diagnostic envelope unwrap round-trip
Property 5: Non-envelope response passthrough

Tag: Feature: sdk-v3-api-upgrade, Property 4: Diagnostic envelope unwrap round-trip
Tag: Feature: sdk-v3-api-upgrade, Property 5: Non-envelope response passthrough
"""

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from aplos_nca_saas_sdk.nca_resources.v3.diagnostic_envelope import (
    DiagnosticEnvelopeHandler,
    ENVELOPE_KEYS,
)

# Strategy for JSON-safe primitive values (no surrogates that break serialization)
json_primitives = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-1_000_000, max_value=1_000_000),
    st.floats(allow_nan=False, allow_infinity=False),
    st.text(
        alphabet=st.characters(blacklist_categories=("Cs",)),
        min_size=0,
        max_size=30,
    ),
)

# Strategy for arbitrary JSON-safe dicts (used as data / diagnostics payloads)
json_safe_dicts = st.dictionaries(
    keys=st.text(
        alphabet=st.characters(
            whitelist_categories=("L", "N"),
            whitelist_characters="_",
        ),
        min_size=1,
        max_size=15,
    ),
    values=json_primitives,
    min_size=0,
    max_size=10,
)


@given(data=json_safe_dicts, diagnostics=json_safe_dicts)
@settings(max_examples=100)
def test_envelope_unwrap_round_trip(
    data: dict, diagnostics: dict
) -> None:
    """Property 4: Diagnostic envelope unwrap round-trip

    **Validates: Requirements 5.1, 5.2, 5.3**

    For any data dict D and diagnostics dict M, wrapping them in a valid
    diagnostic envelope and calling unwrap() must return a result where:
    - The primary payload keys/values from D are present in the result
    - The diagnostics M is accessible via the _diagnostics key
    """
    # Ensure generated data doesn't collide with the _diagnostics key
    # that unwrap() injects, so we can cleanly verify the round-trip.
    assume("_diagnostics" not in data)

    envelope = {
        "data": dict(data),  # copy to avoid mutation issues
        "statusCode": 200,
        "timestamp": "2025-01-01T00:00:00Z",
        "success": True,
        "diagnostics": dict(diagnostics),
    }

    result = DiagnosticEnvelopeHandler.unwrap(envelope)

    # The unwrapped result must contain all original data keys
    for key, value in data.items():
        assert key in result, f"Missing key '{key}' in unwrapped result"
        assert result[key] == value, (
            f"Value mismatch for key '{key}': expected {value!r}, got {result[key]!r}"
        )

    # Diagnostics must be accessible via _diagnostics
    assert "_diagnostics" in result
    assert result["_diagnostics"] == diagnostics


@given(
    partial_dict=st.dictionaries(
        keys=st.text(
            alphabet=st.characters(
                whitelist_categories=("L", "N"),
                whitelist_characters="_",
            ),
            min_size=1,
            max_size=15,
        ),
        values=json_primitives,
        min_size=0,
        max_size=10,
    )
)
@settings(max_examples=100)
def test_non_envelope_passthrough(partial_dict: dict) -> None:
    """Property 5: Non-envelope response passthrough

    **Validates: Requirements 5.4, 5.5**

    For any dict that does NOT contain all five envelope keys,
    unwrap() must return the dict unchanged (identity).
    """
    # Ensure the dict is missing at least one envelope key
    assume(not ENVELOPE_KEYS.issubset(partial_dict.keys()))

    result = DiagnosticEnvelopeHandler.unwrap(partial_dict)

    assert result is partial_dict, (
        "unwrap() should return the exact same dict object for non-envelope responses"
    )
