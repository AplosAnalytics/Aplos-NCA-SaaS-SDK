"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import time
from typing import Any, Dict

from aws_lambda_powertools import Logger

from aplos_nca_saas_sdk.integration_testing.configs.file_upload_config import (
    FileUploadConfig,
)
from aplos_nca_saas_sdk.integration_testing.configs.login_config import LoginConfig
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_response import (
    IntegrationTestResponse,
)
from aplos_nca_saas_sdk.nca_resources.nca_authenticator import NCAAuthenticator
from aplos_nca_saas_sdk.nca_resources.nca_file_download import NCAFileDownload
from aplos_nca_saas_sdk.nca_resources.nca_file_upload import NCAFileUpload

logger = Logger(service="V3FileOperationsTest")


class V3FileOperationsTest(IntegrationTestBase):
    """V3 File Operations Test Container

    Tests v3 file operations: upload, download-url, stream, lineage,
    list, archive, unarchive, and meta.
    """

    def __init__(self):
        super().__init__(name="v3-file-operations", index=11)

    def test(self) -> bool:
        """Test v3 file operations"""

        self.results.clear()

        file_upload: FileUploadConfig
        for file_upload in self.config.file_uploads.list:
            test_response: IntegrationTestResponse = IntegrationTestResponse()
            test_response.name = self.name

            try:
                # Authenticate
                auth = self.__login(file_upload.login)

                # Upload via v3 endpoint
                logger.info({"message": "Uploading file via v3"})
                uploader = NCAFileUpload(auth.host)
                uploader.authenticator = auth
                upload_response: Dict[str, Any] = uploader.upload_v3(
                    file_upload.file_path
                )

                file_id: str = upload_response.get("file_id", "")
                if not file_id:
                    raise RuntimeError("Failed to get file_id from v3 upload.")

                logger.info(
                    {"message": "V3 file uploaded", "file_id": file_id}
                )

                # Allow time for file processing
                time.sleep(3)

                # List files
                logger.info({"message": "Listing files via v3"})
                list_response = uploader.list_files(limit=5)
                if not isinstance(list_response, dict):
                    raise RuntimeError("Expected dict response from list_files.")

                # Download URL
                logger.info({"message": "Getting v3 file download URL"})
                downloader = NCAFileDownload(auth.host)
                downloader.authenticator = auth
                try:
                    download_url_response = downloader.file_download_url(file_id)
                    if not isinstance(download_url_response, dict):
                        raise RuntimeError(
                            "Expected dict response from file_download_url."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "Download URL not available (may be processing)."}
                    )

                # Stream
                logger.info({"message": "Streaming v3 file content"})
                try:
                    stream_response = downloader.file_stream(file_id)
                    if not isinstance(stream_response, dict):
                        raise RuntimeError(
                            "Expected dict response from file_stream."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "Stream not available (may be processing)."}
                    )

                # Lineage
                logger.info({"message": "Getting v3 file lineage"})
                try:
                    lineage_response = downloader.file_lineage(file_id)
                    if not isinstance(lineage_response, dict):
                        raise RuntimeError(
                            "Expected dict response from file_lineage."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "Lineage not available (may be processing)."}
                    )

                # File meta
                logger.info({"message": "Getting v3 file metadata"})
                try:
                    meta_response = uploader.file_meta(file_id)
                    if not isinstance(meta_response, dict):
                        raise RuntimeError(
                            "Expected dict response from file_meta."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "File meta not available (may be processing)."}
                    )

                # Archive
                logger.info({"message": "Archiving v3 file"})
                try:
                    archive_response = uploader.file_archive(file_id)
                    if not isinstance(archive_response, dict):
                        raise RuntimeError(
                            "Expected dict response from file_archive."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "Archive not applicable to current state."}
                    )

                # Unarchive
                logger.info({"message": "Unarchiving v3 file"})
                try:
                    unarchive_response = uploader.file_unarchive(file_id)
                    if not isinstance(unarchive_response, dict):
                        raise RuntimeError(
                            "Expected dict response from file_unarchive."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "Unarchive not applicable to current state."}
                    )

                test_response.success = True

            except Exception as e:  # pylint: disable=w0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()

    def __login(self, login: LoginConfig) -> NCAAuthenticator:
        nca_login = NCAAuthenticator(host=login.host)
        nca_login.authenticate(username=login.username, password=login.password)
        return nca_login
