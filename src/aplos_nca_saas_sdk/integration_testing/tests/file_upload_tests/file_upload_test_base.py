"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import requests
from datetime import datetime, timedelta

from aplos_nca_saas_sdk.utilities.http_utility import HttpUtilities
from aplos_nca_saas_sdk.aws_resources.aws_s3_presigned_payload import S3PresignedPayload
from aplos_nca_saas_sdk.integration_testing.configs.login import TestLogin
from aplos_nca_saas_sdk.integration_testing.integration_test_base import IntegrationTestBase
from aplos_nca_saas_sdk.integration_testing.integration_test_response import IntegrationTestResponse
from aplos_nca_saas_sdk.nca_resources.nca_file_upload import NCAFileUpload
from aplos_nca_saas_sdk.nca_resources.nca_login import NCALogin


class FileUploadTestBase(IntegrationTestBase):

    @property
    def upload_file_path(self) -> str:
        return self._upload_file_path

    def __init__(self, test_name: str, upload_file_path: str):
        if test_name is None or not test_name:
            raise ValueError("test_name is required.")
        if upload_file_path is None or not upload_file_path:
            raise ValueError("upload_file_path is required.")
        self._upload_file_path = upload_file_path
        super().__init__(test_name)

    
    def test(self) -> bool:
        """Test file upload"""

        self.results.clear()

        for login in self.config.logins.list:
            test_response: IntegrationTestResponse = IntegrationTestResponse()
            test_response.name = self.name
            try:
                # Confirm Login
                nca_login = self.__login(login)
                if not nca_login.jwt:
                    test_response.error = "Failed to authenticate"

                # Confirm Upload
                presign_payload = self.__upload(nca_login, self._upload_file_path)
                if presign_payload is None:
                    test_response.error = "Failed to upload"

                # Confirm conversion and download
                success = self.__download(nca_login, presign_payload)
               
               
                    #test_response.response = token
                    #test_response.success = True
            except Exception as e:  # pylint: disable=w0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()

    def __login(self, login : TestLogin) ->  NCALogin:
        nca_login = NCALogin(aplos_saas_domain=login.domain)
        nca_login.authenticate(
            username=login.username, password=login.password
        )
        return nca_login

    def __upload(self, nca_login : NCALogin, upload_file_path: str) -> S3PresignedPayload:
        nca_file_upload = NCAFileUpload(nca_login)
        presign_payload: S3PresignedPayload = nca_file_upload.upload(upload_file_path) 
        return presign_payload

    def __download(self, nca_login: NCALogin, presign_payload: S3PresignedPayload) -> bool:
        getFileDataUrl = nca_login.config.endpoints.file_data(nca_login.cognito.tenant_id, nca_login.cognito.user_id, presign_payload.file_id)
        getFile = nca_login.config.endpoints.file(nca_login.cognito.tenant_id, nca_login.cognito.user_id, presign_payload.file_id)
         
        max_wait_in_minutes: int = 15    
        headers = HttpUtilities.get_headers(nca_login.jwt)
        current_time = datetime.now()
        
        # Create a timedelta object representing 15 minutes
        time_delta = timedelta(minutes=max_wait_in_minutes)
        # Add the timedelta to the current time
        max_time = current_time + time_delta
        response = requests.get(getFile, headers=headers, timeout=30)
        
        return True
             