"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA

No part of this publication may be reproduced, stored or transmitted,
in any form or by any means (electronic, mechanical, photocopying,
recording or otherwise) without prior written permission from Aplos Analytices, Inc.
"""

import os
from typing import List
from pathlib import Path
import importlib
import inspect
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)


class IntegrationTestFactory:
    def __init__(self):
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
            module_name = (
                f"aplos_nca_saas_sdk.integration_testing.tests.{test_file[:-3]}"
            )
            module = importlib.import_module(module_name)

            # Iterate over all attributes in the module
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # Check if the class inherits from the specified base class
                if (
                    issubclass(obj, IntegrationTestBase)
                    and obj is not IntegrationTestBase
                ):
                    # Instantiate the class
                    print(f"registring test class {name}")
                    self.register_test_class(obj)

    @property
    def test_classes(self) -> List[IntegrationTestBase]:
        """Get the test classes"""
        return self.__test_classes

    def register_test_class(self, test_class: IntegrationTestBase):
        """Register a test class"""
        self.__test_classes.append(test_class)
