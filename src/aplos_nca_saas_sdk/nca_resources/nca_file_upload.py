

from aplos_nca_saas_sdk.aws_resources.aws_s3_presigned_payload import S3PresignedPayload
from aplos_nca_saas_sdk.aws_resources.aws_s3_presigned_upload import S3PresignedUpload
from aplos_nca_saas_sdk.nca_resources.nca_login import NCALogin
from aplos_nca_saas_sdk.utilities.http_utility import HttpUtilities


class NCAFileUpload:
    """NCA File Upload"""

    def __init__(self, nca_login: NCALogin) -> None:

        # TODO:// Confirm we can determine logged in state via existence of jwt
        if nca_login is None or nca_login.jwt is None or not nca_login.jwt:
            raise ValueError("Authenticated nca_login is required.")

        self.__api_domain: str = nca_login.domain
        self.__tenant_id: str = nca_login.cognito.tenant_id
        self.__user_id: str = nca_login.cognito.user_id
        self.__jwt: str = nca_login.jwt

    @property
    def api_root(self) -> str:
        """Gets the base url"""
        # TODO:// Consider refactoring this into service method
        if self.__api_domain is None:
            raise RuntimeError("Missing Aplos Api Domain")

        url = HttpUtilities.build_url(self.__api_domain)
        if isinstance(url, str):
            return (
                f"{url}/tenants/{self.__tenant_id}/users/{self.__user_id}"
            )

        raise RuntimeError("Missing Aplos Api Domain")


    def upload(self, input_file_path: str) -> S3PresignedPayload:
        
        if input_file_path is None or not input_file_path:
            raise ValueError("Valid input_file_path is required.")
        
        # TODO: Should we confirm file upload size as we do in UI? Should there be a separate test for this?
        uploader: S3PresignedUpload = S3PresignedUpload(self.__jwt, str(self.api_root))
        presign_payload: S3PresignedPayload = uploader.upload_file(input_file_path)

        return presign_payload



