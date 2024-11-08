from aplos_nca_saas_toolkit.aws_resources.aws_cognito import CognitoAuthenication


class NCALogin:
    """NCA Login"""

    def __init__(self, cognito_client_id: str | None, region: str | None) -> None:
        self.jwt: str
        self.access_token: str | None = None
        self.refresh_token: str | None = None

        self.cognito: CognitoAuthenication = CognitoAuthenication(
            client_id=cognito_client_id, region=region
        )

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> str:
        """_summary_

        Args:
            username (str): the username
            password (str): the users password

        """

        print("\tLogging in.")
        self.jwt = self.cognito.login(username=username, password=password)

        return self.jwt
