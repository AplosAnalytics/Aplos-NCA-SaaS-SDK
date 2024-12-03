import requests
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)


class TestAppConfiguration(IntegrationTestBase):
    """Application Configuration Tests"""

    def __init__(self):
        super().__init__(name="app_configuration")

    def test(self) -> dict:
        """Test loading the application configuration"""
        app_api_domain = self.env_vars.api_domain
        url = f"https://{app_api_domain}/app/configuration"

        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            print(f"App configuration url is working. {url}")
            print(f"App configuration: {response.json()}")
        else:
            print(
                f"App configuration url is not working. Status code: {response.status_code}"
            )
            raise RuntimeError("App configuration url is not working.")

        return response.json()
