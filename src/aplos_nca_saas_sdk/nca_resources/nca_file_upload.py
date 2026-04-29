"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import json
from typing import Any, Dict

import requests

from aplos_nca_saas_sdk.nca_resources._api_base import NCAApiBaseClass
from aplos_nca_saas_sdk.nca_resources.aws_s3_presigned_upload import (
    S3PresignedUrlUpload,
)
from aplos_nca_saas_sdk.utilities.http_utility import HttpUtilities


class NCAFileUpload(NCAApiBaseClass):
    """NCA File Upload"""

    def __init__(self, host: str) -> None:
        super().__init__(host)

    # ------------------------------------------------------------------
    # V3 helpers
    # ------------------------------------------------------------------

    def _get_v3_url(
        self,
        operation: str,
        *,
        resource_id: str | None = None,
        sub_resource: str | None = None,
    ) -> str:
        """Build a v3 endpoint URL via the router strategy."""
        return self.router.strategy.get_endpoint_url(
            operation,
            host=self.host,
            tenant_id=self.authenticator.cognito.tenant_id,
            user_id=self.authenticator.cognito.user_id,
            resource_id=resource_id,
            sub_resource=sub_resource,
        )

    def _process_v3_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Unwrap a v3 diagnostic envelope via the router strategy."""
        return self.router.strategy.process_response(response_data)

    # ------------------------------------------------------------------
    # Existing public API (preserved)
    # ------------------------------------------------------------------

    def upload(
        self,
        input_file_path: str,
        user_name: str | None = None,
        password: str | None = None,
    ) -> Dict[str, Any]:
        """
        Uploads a file to the Aplos NCA Cloud.

        For v3, the presigned-URL request is routed through the v3
        ``files`` endpoint and the response is unwrapped via the
        diagnostic envelope handler.

        Args:
            input_file_path (str): local path to the file
            user_name (str | None): optional username for authentication
            password (str | None): optional password for authentication

        Raises:
            ValueError: When input_file_path is empty or credentials are missing.

        Returns:
            Dict: {"file_id": id, "status_code": 204}
        """
        if input_file_path is None or not input_file_path:
            raise ValueError("Valid input_file_path is required.")

        if not self.authenticator.cognito.jwt:
            if not user_name or not password:
                raise ValueError(
                    "Valid user_name and password are required or you can set the authenticator object."
                )
            self.authenticator.authenticate(username=user_name, password=password)

        uploader: S3PresignedUrlUpload = S3PresignedUrlUpload(self.host)
        uploader.authenticator = self.authenticator

        upload_response: Dict[str, Any] = uploader.upload_file(
            input_file=input_file_path
        )

        return upload_response

    # ------------------------------------------------------------------
    # V3 file operations
    # ------------------------------------------------------------------

    def file_archive(self, file_id: str) -> Dict[str, Any]:
        """Archive a file (v3).

        Calls POST ``/v3/tenants/{tenant_id}/users/{user_id}/files/{file_id}/archive``.

        Args:
            file_id: The file identifier.

        Returns:
            The (unwrapped) archive response.
        """
        url = self._get_v3_url("file_archive", resource_id=file_id)
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.post(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when archiving file.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to archive file: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def file_unarchive(self, file_id: str) -> Dict[str, Any]:
        """Unarchive a file (v3).

        Calls POST ``/v3/tenants/{tenant_id}/users/{user_id}/files/{file_id}/unarchive``.

        Args:
            file_id: The file identifier.

        Returns:
            The (unwrapped) unarchive response.
        """
        url = self._get_v3_url("file_unarchive", resource_id=file_id)
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.post(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when unarchiving file.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to unarchive file: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def file_meta(
        self,
        file_id: str,
        *,
        key: str | None = None,
        preserve_fields: str | None = None,
    ) -> Dict[str, Any]:
        """Retrieve file metadata (v3).

        Calls ``/v3/tenants/{tenant_id}/users/{user_id}/files/{file_id}/meta``
        with optional ``key`` and ``preserveFields`` query parameters.

        Args:
            file_id: The file identifier.
            key: Optional metadata key to filter by.
            preserve_fields: Optional comma-separated field names to preserve.

        Returns:
            The (unwrapped) file metadata response.
        """
        url = self._get_v3_url("file_meta", resource_id=file_id)

        params: Dict[str, str] = {}
        if key is not None:
            params["key"] = key
        if preserve_fields is not None:
            params["preserveFields"] = preserve_fields

        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, params=params, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving file metadata.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get file metadata: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def list_files(
        self,
        *,
        limit: int | None = None,
        next_token: str | None = None,
    ) -> Dict[str, Any]:
        """List files with pagination (v3).

        Calls ``/v3/tenants/{tenant_id}/users/{user_id}/files`` with
        optional ``limit`` and ``nextToken`` query parameters.

        Args:
            limit: Maximum number of files to return per page.
            next_token: Pagination token from a previous response.

        Returns:
            The (unwrapped) file listing response.
        """
        url = self._get_v3_url("files")

        params: Dict[str, str] = {}
        if limit is not None:
            params["limit"] = str(limit)
        if next_token is not None:
            params["nextToken"] = next_token

        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, params=params, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when listing files.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to list files: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def upload_v3(
        self,
        input_file_path: str,
    ) -> Dict[str, Any]:
        """Upload a file via the v3 files endpoint.

        Requests a presigned upload URL from the v3 ``files`` endpoint,
        then delegates the actual S3 upload to :class:`S3PresignedUrlUpload`.
        The presigned-URL response is unwrapped through the diagnostic
        envelope handler.

        The caller must have already authenticated (i.e.
        ``self.authenticator.cognito.jwt`` is set).

        Args:
            input_file_path: Local path to the file to upload.

        Returns:
            Dict containing ``file_id``, ``status_code``, and upload details.
        """
        if not input_file_path:
            raise ValueError("Valid input_file_path is required.")

        url = self._get_v3_url("files")
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)

        body = {"file_name": input_file_path, "method_type": "post"}
        response = requests.post(
            url=url, headers=headers, data=json.dumps(body), timeout=30
        )

        if response.status_code == 403:
            raise PermissionError(
                "403 Forbidden when requesting v3 presigned upload URL."
            )
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get v3 presigned upload URL: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        json_response = self._process_v3_response(response.json())

        # Delegate the actual S3 upload to the existing uploader
        from aplos_nca_saas_sdk.nca_resources.aws_s3_presigned_payload import (
            S3PresignedUrlPayload,
        )

        payload = S3PresignedUrlPayload(json_response)

        uploader = S3PresignedUrlUpload(self.host)
        uploader.authenticator = self.authenticator
        # Use the internal upload method via the payload
        import os

        if not os.path.exists(input_file_path):
            raise FileNotFoundError(
                "The input file cannot be found. Please check the path and try again."
            )

        with open(input_file_path, "rb") as file:
            files = {"file": (input_file_path, file)}
            upload_response = requests.post(
                str(payload.url), data=payload.form_data, files=files, timeout=60
            )

        if upload_response and upload_response.status_code == 204:
            return {
                "status_code": upload_response.status_code,
                "reason": upload_response.reason,
                "details": "File uploaded successfully via v3 endpoint.",
                "file_id": payload.file_id,
            }
        else:
            raise RuntimeError(
                f"Error uploading file via v3: {upload_response.status_code}. "
                f"Response: {upload_response.reason}"
            )
