"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import time
import requests
from datetime import datetime, timedelta

from aplos_nca_saas_sdk.integration_testing.configs.file_upload import FileUpload
from aplos_nca_saas_sdk.integration_testing.configs.login import Login
from aplos_nca_saas_sdk.utilities.http_utility import HttpUtilities
from aplos_nca_saas_sdk.aws_resources.aws_s3_presigned_payload import S3PresignedPayload
from aplos_nca_saas_sdk.integration_testing.integration_test_base import IntegrationTestBase
from aplos_nca_saas_sdk.integration_testing.integration_test_response import IntegrationTestResponse
from aplos_nca_saas_sdk.nca_resources.nca_file_upload import NCAFileUpload
from aplos_nca_saas_sdk.nca_resources.nca_login import NCALogin


class FileUploadTest(IntegrationTestBase):


    def __init__(self):
        super().__init__("file-upload")

    
    def test(self) -> bool:
        """Test file upload"""

        self.results.clear()
        
        for fileupload in self.config.file_uploads.list:
            test_response: IntegrationTestResponse = IntegrationTestResponse()
            test_response.name = self.name
            try:
                # Confirm Login
                nca_login = self.__login(fileupload.login)
                if not nca_login.jwt:
                    test_response.error = "Failed to authenticate"
                else:
                    # Confirm Upload
                    presign_payload = self.__upload(nca_login, fileupload.filepath)
                    if presign_payload is None:
                        test_response.error = "Failed to upload"
                    else:
                        # Confirm conversion and download
                        # Allow time buffer so file data is available
                        time.sleep(3)
                        self.__download(nca_login, presign_payload, test_response)

            except Exception as e:  # pylint: disable=w0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()

    def __login(self, login : Login) ->  NCALogin:
        nca_login = NCALogin(aplos_saas_domain=login.domain)
        nca_login.authenticate(
            username=login.username, password=login.password
        )
        return nca_login

    def __upload(self, nca_login : NCALogin, upload_file_path: str) -> S3PresignedPayload:
        nca_file_upload = NCAFileUpload(nca_login)
        presign_payload: S3PresignedPayload = nca_file_upload.upload(upload_file_path) 
        return presign_payload

    def __download(self, nca_login: NCALogin, 
                   presign_payload: S3PresignedPayload,
                   test_response: IntegrationTestResponse):
        
        getFileDataEndpoint = nca_login.config.endpoints.file_data(nca_login.cognito.tenant_id, nca_login.cognito.user_id, presign_payload.file_id)
        getFileEndpoint = nca_login.config.endpoints.file(nca_login.cognito.tenant_id, nca_login.cognito.user_id, presign_payload.file_id)
         
        max_wait_in_minutes: int = 3    
        headers = HttpUtilities.get_headers(nca_login.jwt)
        current_time = datetime.now()
        
        # Create a timedelta object representing 3 minutes
        time_delta = timedelta(minutes=max_wait_in_minutes)
        # Add the timedelta to the current time
        max_time = current_time + time_delta

        complete = False
        while not complete:
            response = requests.get(getFileEndpoint, headers=headers, timeout=60)
            json_response: dict = response.json()
            errors = []
            errors.extend(json_response.get("errors") or [])
            status = json_response.get("workable_state")
            complete = status == "ready"
            
            if status == "invalid" or len(errors) > 0:
                test_response.success = False
                test_response.error = f"File conversion failed." if len(errors) < 0 else f"File conversion failed with errors ${errors}."
                break
            if complete:
                break
            if not complete:
                time.sleep(5)
            if datetime.now() > max_time:
                test_response.success = False
                test_response.error = f"Timeout attempting to get conversion file status."
                break 
            
        if test_response.error is not None:
            return

        file_response = requests.get(getFileDataEndpoint, headers=headers, timeout=30)

        json_file_response: dict = file_response.json() 
        data = json_file_response.get("data", None)   
        error = json_file_response.get("error", None)
        
        if data is None:
            test_response.success = False
            test_response.error = f"File download missing expected data. "
        if error is not None:
            test_response.success = False
            test_response.error =  (test_response.error or "") + f"File download contained error ${error}"
        
        test_response.success = True    

             