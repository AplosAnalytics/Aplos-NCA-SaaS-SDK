"""
Property 1: Unsupported version rejection

For any string that is not a recognized API version (i.e., not "v1" or "v3"),
calling ApiClientFactory.create(version) SHALL raise a ValueError whose message
contains the list of supported versions.

**Validates: Requirements 1.4**
Tag: Feature: sdk-v3-api-upgrade, Property 1: Unsupported version rejection
"""

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Ensure v1 and v3 strategies are registered
import aplos_nca_saas_sdk.nca_resources.v1  # noqa: F401
import aplos_nca_saas_sdk.nca_resources.v3  # noqa: F401
from aplos_nca_saas_sdk.nca_resources.api_client_factory import ApiClientFactory

SUPPORTED_VERSIONS = {"v1", "v3"}


@given(version=st.text(min_size=1))
@settings(max_examples=100)
def test_unsupported_version_raises_value_error(version: str) -> None:
    """Property 1: Unsupported version rejection

    **Validates: Requirements 1.4**

    For any non-empty string that is NOT a supported version,
    ApiClientFactory.create() must raise ValueError with supported
    versions listed in the message.
    Empty strings are excluded because the factory treats them as
    "no version provided" and falls back to the default (v1).
    """
    assume(version not in SUPPORTED_VERSIONS)

    with pytest.raises(ValueError, match="Supported versions:"):
        ApiClientFactory.create(version)
