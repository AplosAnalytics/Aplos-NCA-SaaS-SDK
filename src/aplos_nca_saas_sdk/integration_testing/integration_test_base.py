from aplos_nca_saas_sdk.utilities.environment_vars import EnvironmentVars
from aplos_nca_saas_sdk.nca_resources.nca_endpoints import NCAEndpoints


class IntegrationTestBase:
    def __init__(self, name: str, index: int = 0):
        self.name = name
        self.index = index
        self.env_vars: EnvironmentVars = EnvironmentVars()

        if not self.env_vars.api_domain:
            raise RuntimeError(
                "APLOS_API_DOMAIN environment variable is not set. "
                "This is required to run the tests"
            )

        self.endpoints: NCAEndpoints = NCAEndpoints(
            domain=self.env_vars.api_domain,
        )

    def test(self):
        """Run the Test"""
        raise RuntimeError("This should be implemented by the subclass.")
