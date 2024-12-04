from typing import Any, Dict

from aplos_nca_saas_sdk.nca_resources.nca_login import NCALogin

from aplos_nca_saas_sdk.nca_resources.nca_app_configuration import (
    NCAAppConfiguration,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)


class TestAppLogin(IntegrationTestBase):
    """Application Configuration Tests"""

    def __init__(self):
        super().__init__("app-login")

    def test(self) -> dict:
        """Test a login"""

        # get the configuration
        config: NCAAppConfiguration = NCAAppConfiguration(self.env_vars.api_domain)
        response = config.get()

        # "idp": {
        #         "Auth": {
        #         "Cognito": {
        #             "region": "<region>",
        #             "userPoolId": "<user-pool-id>",
        #             "userPoolClientId": "<user-pool-client-id>",
        #             "authenticationFlowType": "<auth-flow-type>"
        #         }
        #         }
        #     },
        data: Dict[str, Any] = response.json()
        cognito_client_id = (
            data.get("idp", {})
            .get("Auth", {})
            .get("Cognito", {})
            .get("userPoolClientId")
        )
        cognito_region = (
            data.get("idp", {}).get("Auth", {}).get("Cognito", {}).get("region")
        )

        if cognito_client_id is None:
            raise RuntimeError("Failed to get cognito client id")
        if cognito_region is None:
            raise RuntimeError("Failed to get cognito region")

        user_name = self.env_vars.username
        password = self.env_vars.password

        login = NCALogin(cognito_client_id=cognito_client_id, region=cognito_region)
        token = login.authenticate(username=user_name, password=password)
        if not token:
            raise RuntimeError("Failed to authenticate")
        else:
            print("Successfully authenticated")
            return {"token": token}
