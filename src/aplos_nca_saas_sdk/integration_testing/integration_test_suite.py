"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA

No part of this publication may be reproduced, stored or transmitted,
in any form or by any means (electronic, mechanical, photocopying,
recording or otherwise) without prior written permission from Aplos Analytices, Inc.
"""

from aplos_nca_saas_sdk.integration_testing.integration_test_factory import (
    IntegrationTestFactory,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)


class IntegrationTestSuite:
    """Runs Tests against an active instance"""

    def __init__(self):
        pass

    def test(self):
        """Run a full suite of integration tests"""

        factory: IntegrationTestFactory = IntegrationTestFactory()
        test_class: IntegrationTestBase | None = None
        for test_class in factory.test_classes:
            test_instance: IntegrationTestBase = test_class()
            print(f"Running test class {test_instance.name}")
            test_instance.test()
