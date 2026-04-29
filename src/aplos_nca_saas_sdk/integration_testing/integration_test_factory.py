"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import os
from typing import List, Optional
from pathlib import Path
import importlib
import inspect
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)
from aplos_nca_saas_sdk.integration_testing.tests.file_upload_test import FileUploadTest


class IntegrationTestFactory:
    """
    Integration Test Factory
    Loads all the integration tests from the tests directory and registers them for execution.
    Supports version-aware filtering: v3-prefixed test files only run when api_version == "v3".
    """

    def __init__(self, api_version: Optional[str] = None):
        self.__api_version: str = api_version or "v1"
        self.__test_classes: List[IntegrationTestBase] = []
        self.__load_all_classes()

    def __load_all_classes(self):
        # find all files in the test directory that end in _test.py
        test_directory = os.path.join(Path(__file__).parent, "tests")
        potential_test_files = os.listdir(test_directory)
        test_files = [
            f
            for f in potential_test_files
            if f.endswith("_test.py") and f != "__init__.py"
        ]

        # load the class dynamically
        for test_file in test_files:
            # v3-prefixed test files only run when api_version is "v3"
            if test_file.startswith("v3_") and self.__api_version != "v3":
                continue

            module_name = (
                f"aplos_nca_saas_sdk.integration_testing.tests.{test_file[:-3]}"
            )
            module = importlib.import_module(module_name)

            # Iterate over all attributes in the module
            for _, obj in inspect.getmembers(module, inspect.isclass):
                # Check if the class inherits from the specified base class
                if (
                    issubclass(obj, IntegrationTestBase)
                    and obj is not IntegrationTestBase
                ):
                    # Instantiate the class and store it
                    self.register_test_instance(obj())

    @property
    def api_version(self) -> str:
        """Get the API version used for test filtering"""
        return self.__api_version

    @property
    def test_instances(self) -> List[IntegrationTestBase]:
        """Get the test classes"""
        self.__test_classes.sort(key=lambda x: x.index)
        return self.__test_classes

    def register_test_instance(self, test_class: IntegrationTestBase):
        """Register a test class"""
        self.__test_classes.append(test_class)
