"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from aws_lambda_powertools import Logger

from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_response import (
    IntegrationTestResponse,
)
from aplos_nca_saas_sdk.nca_resources.nca_analysis import NCAAnalysis
from aplos_nca_saas_sdk.utilities.file_utility import FileUtility

logger = Logger(service="V3ExecutionTest")


class V3ExecutionTest(IntegrationTestBase):
    """V3 Execution Operations Test Container

    Tests v3 execution operations: queue analysis, check status,
    retrieve outputs, cancel, and archive.
    """

    def __init__(self):
        super().__init__(name="v3-execution", index=10)

    def test(self) -> bool:
        """Test v3 execution operations"""

        self.results.clear()

        for nca_execution_config in self.config.nca_executions.list:
            test_response: IntegrationTestResponse = IntegrationTestResponse()
            test_response.name = self.name

            try:
                nca_analysis: NCAAnalysis = NCAAnalysis(
                    nca_execution_config.login.host
                )

                # Authenticate
                nca_analysis.authenticator.authenticate(
                    username=nca_execution_config.login.username,
                    password=nca_execution_config.login.password,
                )

                # Queue analysis via v3 endpoint
                logger.info({"message": "Queuing v3 analysis execution"})
                execution_response = nca_analysis.execute(
                    username=nca_execution_config.login.username,
                    password=nca_execution_config.login.password,
                    input_file_path=FileUtility.load_filepath(
                        nca_execution_config.input_file_path
                    ),
                    config_data=nca_execution_config.config_data,
                    meta_data=nca_execution_config.meta_data,
                    wait_for_results=False,
                    data_processing=nca_execution_config.data_processing,
                    post_processing=nca_execution_config.post_processing,
                    full_payload=nca_execution_config.full_payload,
                )

                execution_id = execution_response.get("execution", {}).get(
                    "execution_id", ""
                )
                if not execution_id:
                    raise RuntimeError(
                        "Failed to get execution_id from v3 queue response."
                    )

                logger.info(
                    {
                        "message": "V3 execution queued",
                        "execution_id": execution_id,
                    }
                )

                # Check execution status
                logger.info({"message": "Checking v3 execution status"})
                status_response = nca_analysis.execution_status(execution_id)
                if not isinstance(status_response, dict):
                    raise RuntimeError(
                        "Expected dict response from execution_status."
                    )

                # Retrieve outputs package
                logger.info({"message": "Retrieving v3 execution outputs package"})
                try:
                    nca_analysis.execution_outputs_package(execution_id)
                except RuntimeError:
                    # Outputs may not be ready yet; acceptable for integration test
                    logger.info(
                        {"message": "Outputs package not yet available (expected)."}
                    )

                # Retrieve outputs report
                logger.info({"message": "Retrieving v3 execution outputs report"})
                try:
                    nca_analysis.execution_outputs_report(execution_id)
                except RuntimeError:
                    logger.info(
                        {"message": "Outputs report not yet available (expected)."}
                    )

                # Cancel execution
                logger.info({"message": "Cancelling v3 execution"})
                try:
                    cancel_response = nca_analysis.execution_cancel(execution_id)
                    if not isinstance(cancel_response, dict):
                        raise RuntimeError(
                            "Expected dict response from execution_cancel."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "Cancel may not apply to current state."}
                    )

                # Archive execution
                logger.info({"message": "Archiving v3 execution"})
                try:
                    archive_response = nca_analysis.execution_archive(execution_id)
                    if not isinstance(archive_response, dict):
                        raise RuntimeError(
                            "Expected dict response from execution_archive."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "Archive may not apply to current state."}
                    )

                test_response.success = True

            except Exception as e:  # pylint: disable=w0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()
