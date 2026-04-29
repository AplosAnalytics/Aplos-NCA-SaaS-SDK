"""
Property test for NCAAppConfiguration Cognito configuration extraction.

Property 7: Cognito configuration extraction

Tag: Feature: sdk-v3-api-upgrade, Property 7: Cognito configuration extraction
"""

import json
from unittest.mock import MagicMock, patch

from hypothesis import given, settings
from hypothesis import strategies as st

from aplos_nca_saas_sdk.nca_resources.nca_app_configuration import NCAAppConfiguration

# Strategy for non-empty alphanumeric strings (simulating userPoolClientId and region)
cognito_strings = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "Pd")),
    min_size=1,
    max_size=60,
)


@st.composite
def cognito_config_responses(draw: st.DrawFn) -> tuple:
    """Generate a config response JSON containing idp.Auth.Cognito with random
    userPoolClientId and region values.

    Returns (response_dict, expected_client_id, expected_region).
    """
    client_id = draw(cognito_strings)
    region = draw(cognito_strings)

    response_body = {
        "idp": {
            "Auth": {
                "Cognito": {
                    "userPoolClientId": client_id,
                    "region": region,
                    "userPoolId": "us-east-1_XXXXXX",
                    "authenticationFlowType": "USER_SRP_AUTH",
                }
            }
        }
    }
    return response_body, client_id, region


@given(data=cognito_config_responses())
@settings(max_examples=200)
def test_cognito_configuration_extraction(data: tuple) -> None:
    """Property 7: Cognito configuration extraction

    **Validates: Requirements 11.4**

    For any valid configuration response JSON containing an
    idp.Auth.Cognito section with userPoolClientId and region fields,
    NCAAppConfiguration.cognito_client_id and .cognito_region SHALL
    return the exact values from those fields.
    """
    response_body, expected_client_id, expected_region = data

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = response_body

    with patch("requests.get", return_value=mock_response):
        config = NCAAppConfiguration(host="api.example.com")
        # Reset cached response so each hypothesis example gets a fresh call
        config._NCAAppConfiguration__response = None
        config._NCAAppConfiguration__response = None

        # Patch again for the actual property access (get() caches)
        with patch("requests.get", return_value=mock_response):
            config2 = NCAAppConfiguration(host="api.example.com")

            assert config2.cognito_client_id == expected_client_id, (
                f"Expected cognito_client_id={expected_client_id!r}, "
                f"got {config2.cognito_client_id!r}"
            )
            assert config2.cognito_region == expected_region, (
                f"Expected cognito_region={expected_region!r}, "
                f"got {config2.cognito_region!r}"
            )
