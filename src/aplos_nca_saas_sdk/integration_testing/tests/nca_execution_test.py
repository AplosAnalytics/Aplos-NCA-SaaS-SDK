"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""


import json
from pathlib import Path
from aws_lambda_powertools import Logger
from typing import Any, Dict
from aplos_nca_saas_sdk.integration_testing.integration_test_base import IntegrationTestBase
from aplos_nca_saas_sdk.integration_testing.integration_test_response import IntegrationTestResponse
from aplos_nca_saas_sdk.nca_resources.nca_executions import NCAExecution

logger = Logger(service="NCAExecutionTest")

class NCAExecutionTest(IntegrationTestBase):
    """NCA Execution Test Container"""

    def __init__(self):
        super().__init__("nca-execution")

    def test(self) -> bool:
        """Test Engine Execution"""

        self.results.clear()

        for nca_execution_config in self.config.nca_executions.list:
            test_response: IntegrationTestResponse = IntegrationTestResponse()
            test_response.name = self.name
            logger.info({"message": "Creating NCAExecution for input file.", "file": nca_execution_config.input_file_path})
            try:
                # Create new NCA Execution
                nca_execution = self.createNCAExecution(nca_execution_config.login.domain, None, None)
                
                # Initialize Configuration Data
                config_data: Dict[str, Any] = {}
                if isinstance(nca_execution_config.config_data, str):
                    logger.info({"message": "Initializing config_data from file", "config_data": nca_execution_config.config_data})
                    with open(nca_execution_config.config_data, "r", encoding="utf-8") as f:
                        config_data = json.load(f)
                elif isinstance(nca_execution_config.config_data, Dict):
                    logger.info({"message": "Initializing config_data from Object."})
                    config_data = nca_execution_config.config_data
                else: 
                     raise RuntimeError("Missing required config_data for NCAExecution.")
                
                # Execute, the execution should raise errors that will fail the test
                logger.info({"message": "Invoking Execution"})
                expected_output_file = nca_execution.execute(
                    username=nca_execution_config.login.username, 
                    password=nca_execution_config.login.password,
                    input_file_path=nca_execution_config.input_file_path,
                    config_data=config_data,
                    meta_data=nca_execution_config.meta_data,
                    wait_for_results=True,
                    output_directory=nca_execution_config.output_dir,
                    unzip_after_download=False)
                
                # Verify Download
                logger.info({"message": "Execution complete. Verifying results download."})
                if expected_output_file is None:
                    raise RuntimeError("Expected populated output_file from NCAExecution was None.")
                elif not Path(expected_output_file).is_file:
                    raise RuntimeError("Expected downloaded file does not exist.")
                    
            except Exception as e:  # pylint: disable=w0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()
    
    def createNCAExecution(self, api_domain: str | None, cognito_client_id: str | None, region: str | None) -> NCAExecution:
        nca_execution = NCAExecution(api_domain, cognito_client_id, region)
        return nca_execution