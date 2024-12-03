from aplos_nca_saas_sdk.utilities.environment_vars import EnvironmentVars


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

    def test(self):
        """Run the Test"""
        raise RuntimeError("This should be implemented by the subclass.")
