"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import time
from datetime import datetime, timedelta
from typing import Any, Dict

import requests
from aws_lambda_powertools import Logger
from aplos_nca_saas_sdk.nca_resources._api_base import NCAApiBaseClass

logger = Logger(service="nca-validations")


class NCAValidation(NCAApiBaseClass):
    """NCA Analysis Validation API"""

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

    def execute(
        self,
        username: str,
        password: str,
        wait_for_results: bool = True,
        max_wait_in_seconds: int = 900,
    ) -> Dict[str, Any]:
        """
        Runs a validation

        Args:
            username (str): username
            password (str): password

        Returns:
            Dict[str, Any]: response object
        """

        self.authenticator.authenticate(username=username, password=password)

        # Route to v3 validations endpoint when api_version is "v3"
        if self.api_version == "v3":
            url = self._get_v3_url("validations")
        else:
            url = self.endpoints.validations

        # no payload required
        headers = self.authenticator.get_jwt_http_headers()
        validation_post_response = requests.post(url, headers=headers, timeout=30)

        if validation_post_response.status_code != 200:
            raise RuntimeError(
                f"Failed to execution a validation batch. Status Code: {validation_post_response.status_code}"
                f"Reason: {validation_post_response.reason}"
            )

        response = {
            "queued": validation_post_response.json()
            if self.api_version != "v3"
            else self._process_v3_response(validation_post_response.json()),
            "results": None,
        }

        if wait_for_results:
            batch_id = (
                response["queued"].get("validation_batch", {}).get("id")
            )

            if not batch_id:
                raise RuntimeError(
                    "Failed to get the validation batch id from the response."
                )
            completed = False
            current_time = datetime.now()
            # Create a timedelta object representing 15 minutes
            time_delta = timedelta(seconds=max_wait_in_seconds)
            # Add the timedelta to the current time
            max_time = current_time + time_delta
            while not completed:
                # Route to v3 validation endpoint when api_version is "v3"
                if self.api_version == "v3":
                    validation_url = self._get_v3_url(
                        "validation", resource_id=batch_id
                    )
                else:
                    validation_url = self.endpoints.validation(batch_id=batch_id)

                validation_get_response = requests.get(
                    validation_url,
                    timeout=30,
                    headers=self.authenticator.get_jwt_http_headers(),
                )
                if validation_get_response.status_code != 200:
                    raise RuntimeError(
                        f"Failed to get validation results. Status Code: {validation_get_response.status_code}"
                        f"Reason: {validation_get_response.reason}"
                    )

                json_response = validation_get_response.json()

                # Process v3 response through diagnostic envelope handler
                if self.api_version == "v3":
                    json_response = self._process_v3_response(json_response)

                status = json_response.get("status")
                completed = status == "complete"

                if not completed:
                    if datetime.now() > max_time:
                        raise RuntimeError(
                            "Timeout attempting to get validation results. "
                            f"The current timeout limit is {max_wait_in_seconds} seconds. "
                            "You may need to up the timeout period, or check for errors. "
                        )
                    logger.info(f"waiting for results.... {status}")
                    time.sleep(15)
                else:
                    response["results"] = json_response

        logger.info("Validation complete.")
        return response
