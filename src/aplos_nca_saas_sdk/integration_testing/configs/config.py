"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import json
from typing import Any, Dict
from aplos_nca_saas_sdk.integration_testing.configs.app_config import (
    TestApplicationConfiguration,
)
from aplos_nca_saas_sdk.integration_testing.configs.login import TestLogins


class TestConfiguration:
    """
    Testing Suite Configuration: Provides a way to define the testing configuration for the Aplos Analytics SaaS SDK

    """

    def __init__(self):
        self.app_config: TestApplicationConfiguration = TestApplicationConfiguration()
        self.logins: TestLogins = TestLogins()

    def load(self, file_path: str):
        """
        Loads the configuration from a file

        :param file_path: The path to the configuration file
        :return: None
        """

        config: Dict[str, Any] = {}
        with open(file_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.logins.load(config.get("login_test", {}))
        self.app_config.load(config.get("application_config_test", {}))
