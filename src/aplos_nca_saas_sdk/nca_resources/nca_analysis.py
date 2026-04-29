"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import json
import os
import time
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict

import requests
from aws_lambda_powertools import Logger

from aplos_nca_saas_sdk.nca_resources._api_base import NCAApiBaseClass
from aplos_nca_saas_sdk.nca_resources.aws_s3_presigned_upload import (
    S3PresignedUrlUpload,
)
from aplos_nca_saas_sdk.utilities.environment_vars import EnvironmentVars
from aplos_nca_saas_sdk.utilities.http_utility import HttpUtilities

logger = Logger()


class NCAAnalysis(NCAApiBaseClass):
    """NCA Analysis API"""

    def __init__(self, host: str) -> None:
        super().__init__(host)

        self.verbose: bool = False

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

    def execute(
        self,
        username: str,
        password: str,
        input_file_path: str,
        config_data: dict,
        *,
        meta_data: str | dict | None = None,
        post_processing: str | dict | None = None,
        data_processing: str | dict | None = None,
        wait_for_results: bool = True,
        max_wait_in_seconds: int = 900,
        output_directory: str | None = None,
        unzip_after_download: bool = False,
        full_payload: str | dict | None = None
    ) -> Dict[str, Any]:
        """
        Executes an analysis.
            - Uploads an analysis file.
            - Adds the execution to the queue.

        Args:
            username (str): the username
            password (str): the users password
            input_file_path (str): the path to the input (analysis) file
            config_data (dict): analysis configuration information
            meta_data (str | dict | None, optional): meta data attached to the execution. Defaults to None.
            wait_for_results (bool, optional): should the program wait for results. Defaults to True.
            max_wait_in_seconds (int optional): the max time to wait for a download
            output_directory (str, optional): the output directory. Defaults to None (the local directory is used)
            unzip_after_download (bool): Results are downloaded as a zip file, this option will unzip them automatically.  Defaults to False

        Returns:
            Dict[str, Any]: The execution response.  If you wait for the completion
        """

        self.log(f"\tLogging into {self.host}.")

        self.authenticator.authenticate(username=username, password=password)

        self.log("\tUploading the analysis file.")
        uploader: S3PresignedUrlUpload = S3PresignedUrlUpload(str(self.host))
        uploader.authenticator = self.authenticator
        upload_response: Dict[str, Any] = uploader.upload_file(input_file_path)

        file_id: str = upload_response.get("file_id", "")
        if not file_id:
            raise RuntimeError(
                "Unexpected empty file_id when attempting to upload file."
            )

        self.log("\tAdding analysis to the queue.")
        execution_response: Dict[str, Any] = self.__add_to_queue(
            file_id=file_id,
            config_data=config_data,
            meta_data=meta_data,
            post_processing=post_processing,
            data_processing=data_processing,
            full_payload=full_payload
        )

        execution_id: str = execution_response.get("execution_id", "")

        response = {
            "execution": execution_response,
            "upload": upload_response,
            "results": {"file": None},
        }

        if not execution_id:
            raise RuntimeError(
                "Unexpected empty execution_id when attempting to execute analysis."
            )

        if wait_for_results:
            # wait for it
            download_url = self.wait_for_results(
                execution_id=execution_id, max_wait_in_seconds=max_wait_in_seconds
            )
            # download the files
            if download_url is None:
                raise RuntimeError(
                    "Unexpected empty download_url when attempting to download results."
                )
            else:
                self.log("\tDownloading the results.")
                file_path = self.download_file(
                    download_url,
                    output_directory=output_directory,
                    do_unzip=unzip_after_download,
                )

                response["results"]["file"] = file_path
        else:
            self.log("Bypassed results download.")
            response["results"]["status_code"] = 201
            response["results"]["message"] = "Waiting for results download bypassed. Running Fast Executions."
        return response

    def __add_to_queue(
        self,
        file_id: str,
        config_data: dict,
        meta_data: str | dict | None = None,
        post_processing: str | dict | None = None,
        data_processing: str | dict | None = None,
        full_payload: str | dict | None = None
    ) -> Dict[str, Any]:
        """
        Adds the analysis to the execution queue.

        For v3, submits to the ``analysis_queue`` endpoint and processes
        the response through the diagnostic envelope handler.

        Args:
            file_id (str): the uploaded file id
            config_data (dict): the config_data for the analysis file
            meta_data (str | dict): Optional.  Any meta data you'd like attached to this execution
        Returns:
            Dict[str, Any]: the api response
        """

        if not file_id:
            raise ValueError("Missing file_id.  Please provide a valid file_id.")

        if not config_data:
            raise ValueError(
                "Missing config_data.  Please provide a valid config_data."
            )
        headers = self.authenticator.get_jwt_http_headers()

        submission: Dict[str, Any] = {}

        if full_payload:
            submission = full_payload
            # we still need to add the file id at this point
            submission["file"] = {"id": file_id}
        else:
            submission = {
                "file": {"id": file_id},
                "configuration": config_data,
                "meta_data": meta_data,
                "post_processing": post_processing,
                "data_processing": data_processing
            }

        # Route to v3 analysis_queue endpoint when api_version is "v3"
        if self.api_version == "v3":
            url = self._get_v3_url("analysis_queue")
        else:
            url = self.endpoints.executions

        response: requests.Response = requests.post(
            url,
            headers=headers,
            data=json.dumps(submission),
            timeout=30,
        )
        json_response: dict = response.json()

        if response.status_code == 403:
            raise PermissionError(
                "Failed to execute.  A 403 response occurred.  "
                "This could a token issue or a url path issue  "
                "By default unknown gateway calls return 403 errors. "
            )
        elif response.status_code != 200:
            raise RuntimeError(
                f"Unknown Error occurred during executions: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        # Process v3 response through diagnostic envelope handler
        if self.api_version == "v3":
            json_response = self._process_v3_response(json_response)

        execution_id = str(json_response.get("execution_id"))

        self.log(f"\tExecution {execution_id} started.")

        return json_response

    def wait_for_results(
        self, execution_id: str, max_wait_in_seconds: float = 900
    ) -> str | None:
        """
        Wait for results.

        For v3, polls the ``execution_status`` endpoint and processes
        responses through the diagnostic envelope handler.

        Args:
            execution_id (str): the analysis execution id

        Returns:
            str | None: on success: a url for download, on failure: None
        """

        if self.api_version == "v3":
            url = self._get_v3_url("execution_status", resource_id=execution_id)
        else:
            url = f"{self.endpoints.execution(execution_id)}"

        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        current_time = datetime.now()
        # Create a timedelta object representing 15 minutes
        time_delta = timedelta(seconds=max_wait_in_seconds)

        # Add the timedelta to the current time
        max_time = current_time + time_delta

        complete = False
        while not complete:
            response = requests.get(url, headers=headers, timeout=30)
            json_response: dict = response.json()

            # Process v3 response through diagnostic envelope handler
            if self.api_version == "v3":
                json_response = self._process_v3_response(json_response)

            status = json_response.get("status")
            complete = status == "complete"
            elapsed = (
                json_response.get("times", {}).get("elapsed", "0:00:00") or "--:--"
            )
            if status == "failed" or complete:
                break
            if not complete:
                self.log(f"\t\twaiting for results.... {status}: {elapsed}")
                time.sleep(5)
            if datetime.now() > max_time:
                status = "timeout"
                break
            if status is None and elapsed is None:
                # we have a problem
                status = "unknown issue"
                break

        if status == "complete":
            self.log("\tExecution complete.")
            self.log(f"\tExecution duration = {elapsed}.")
            return json_response["presigned"]["url"]
        else:
            raise RuntimeError(
                f"\tExecution failed. Execution ID = {execution_id}. reason: {json_response.get('errors')}"
            )

    def download_file(
        self,
        presigned_download_url: str,
        output_directory: str | None = None,
        do_unzip: bool = False,
    ) -> str | None:
        """
        # Step 5
        Download completed analysis files

        Args:
            presigned_download_url (str): presigned download url
            output_directory (str | None): optional output directory

        Returns:
            str: file path to results or None
        """
        if output_directory is None:
            output_directory = str(Path(__file__).parent.parent)
            output_directory = os.path.join(output_directory, ".aplos-nca-output")

        if EnvironmentVars.is_running_in_aws_lambda():
            # /tmp is the only directory we can write to unless we mount an external drive
            # TODO: allow for external mapped drives, perhaps test if we can write to it

            output_directory = os.path.join("/tmp", ".aplos-nca-output")

            self.log(
                f"\t\tRunning in AWS Lambda.  Setting output directory to {output_directory}"
            )

        output_file = f"results-{time.strftime('%Y-%m-%d-%Hh%Mm%Ss')}.zip"

        output_file = os.path.join(output_directory, output_file)
        os.makedirs(output_directory, exist_ok=True)

        response = requests.get(presigned_download_url, timeout=60)
        # write the zip to a file
        with open(output_file, "wb") as f:
            f.write(response.content)

        # optionally, extract all the files from the zip
        if do_unzip:
            with zipfile.ZipFile(output_file, "r") as zip_ref:
                zip_ref.extractall(output_file.replace(".zip", ""))

        unzipped_state = "and unzipped" if do_unzip else "in zip format"

        self.log(f"\tResults file downloaded {unzipped_state}.")
        self.log(f"\t\tResults are available in: {output_directory}")

        return output_file

    # ------------------------------------------------------------------
    # V3 execution operations
    # ------------------------------------------------------------------

    def execution_status(self, execution_id: str) -> Dict[str, Any]:
        """Retrieve execution status (v3).

        Calls ``/v3/tenants/{tenant_id}/users/{user_id}/executions/{execution_id}/status``.

        Args:
            execution_id: The execution identifier.

        Returns:
            The (unwrapped) status response.
        """
        url = self._get_v3_url("execution_status", resource_id=execution_id)
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving execution status.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get execution status: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def execution_config(self, execution_id: str) -> Dict[str, Any]:
        """Retrieve execution configuration (v3).

        Calls ``/v3/tenants/{tenant_id}/users/{user_id}/executions/{execution_id}/config``.

        Args:
            execution_id: The execution identifier.

        Returns:
            The (unwrapped) config response.
        """
        url = self._get_v3_url("execution_config", resource_id=execution_id)
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving execution config.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get execution config: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def execution_outputs_package(self, execution_id: str) -> Dict[str, Any]:
        """Retrieve execution outputs package (v3).

        Calls ``/v3/tenants/{tenant_id}/users/{user_id}/executions/{execution_id}/outputs/package``.

        Args:
            execution_id: The execution identifier.

        Returns:
            The (unwrapped) outputs package response.
        """
        url = self._get_v3_url("execution_outputs_package", resource_id=execution_id)
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving outputs package.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get execution outputs package: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def execution_outputs_report(self, execution_id: str) -> Dict[str, Any]:
        """Retrieve execution outputs report (v3).

        Calls ``/v3/tenants/{tenant_id}/users/{user_id}/executions/{execution_id}/outputs/report``.

        Args:
            execution_id: The execution identifier.

        Returns:
            The (unwrapped) outputs report response.
        """
        url = self._get_v3_url("execution_outputs_report", resource_id=execution_id)
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving outputs report.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get execution outputs report: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def execution_cancel(self, execution_id: str) -> Dict[str, Any]:
        """Cancel an execution (v3).

        Calls POST ``/v3/tenants/{tenant_id}/users/{user_id}/executions/{execution_id}/cancel``.

        Args:
            execution_id: The execution identifier.

        Returns:
            The (unwrapped) cancel response.
        """
        url = self._get_v3_url("execution_cancel", resource_id=execution_id)
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.post(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when cancelling execution.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to cancel execution: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def execution_archive(self, execution_id: str) -> Dict[str, Any]:
        """Archive an execution (v3).

        Calls POST ``/v3/tenants/{tenant_id}/users/{user_id}/executions/{execution_id}/archive``.

        Args:
            execution_id: The execution identifier.

        Returns:
            The (unwrapped) archive response.
        """
        url = self._get_v3_url("execution_archive", resource_id=execution_id)
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.post(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when archiving execution.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to archive execution: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    def execution_output_by_type(
        self, execution_id: str, output_type: str
    ) -> Dict[str, Any]:
        """Retrieve a specific execution output by type (v3).

        Calls ``/v3/tenants/{tenant_id}/users/{user_id}/executions/{execution_id}/outputs/type/{output_type}``.

        Args:
            execution_id: The execution identifier.
            output_type: The output type to retrieve.

        Returns:
            The (unwrapped) output response.
        """
        url = self._get_v3_url(
            "execution_output_by_type",
            resource_id=execution_id,
            sub_resource=output_type,
        )
        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 403:
            raise PermissionError("403 Forbidden when retrieving output by type.")
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get execution output by type: {response.status_code}. "
                f"Reason: {response.reason}"
            )

        return self._process_v3_response(response.json())

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def log(self, message: str | Dict[str, Any]):
        """Log the message"""
        logger.debug(message)

        if isinstance(message, dict):
            message = json.dumps(message, indent=2)

        if self.verbose:
            print(message)
