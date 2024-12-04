"""
Aplos Analytics
"""

from aplos_nca_saas_sdk.nca_resources.nca_app_configuration import (
    NCAAppConfiguration,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)


class TestAppConfiguration(IntegrationTestBase):
    """Application Configuration Tests"""

    def __init__(self):
        super().__init__(name="app_configuration")

    def test(self) -> dict:
        """Test loading the application configuration"""
        url = self.endpoints.app_configuration()

        config: NCAAppConfiguration = NCAAppConfiguration(self.env_vars.api_domain)
        response = config.get()

        if response.status_code == 200:
            print(f"App configuration url is working. {url}")
            print(f"App configuration: {response.json()}")
        else:
            print(
                f"App configuration url is not working. Status code: {response.status_code}"
            )
            raise RuntimeError("App configuration url is not working.")

        return response.json()
