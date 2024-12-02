from aplos_nca_saas_sdk.nca_resources.nca_login import NCALogin
from aplos_nca_saas_sdk.utilities.environment_vars import EnvironmentVars


class TestAppLogin:
    """Application Configuration Tests"""

    def __init__(self):
        pass

    def test(self, env_vars: EnvironmentVars) -> dict:
        """Test a login"""
        cognito_client_id = env_vars.client_id
        cognito_region = env_vars.aws_region
        user_name = env_vars.username
        password = env_vars.password
        login = NCALogin(cognito_client_id=cognito_client_id, region=cognito_region)
        token = login.authenticate(username=user_name, password=password)
        if not token:
            raise RuntimeError("Failed to authenticate")
        else:
            print("Successfully authenticated")
            return {"token": token}
