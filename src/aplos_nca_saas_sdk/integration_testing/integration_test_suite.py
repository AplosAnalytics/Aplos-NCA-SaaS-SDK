"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA

No part of this publication may be reproduced, stored or transmitted,
in any form or by any means (electronic, mechanical, photocopying,
recording or otherwise) without prior written permission from Aplos Analytices, Inc.
"""

from aplos_nca_saas_sdk.integration_testing.tests.test_app_configuration import (
    TestAppConfiguration,
)
from aplos_nca_saas_sdk.integration_testing.tests.test_app_login import (
    TestAppLogin,
)
from aplos_nca_saas_sdk.utilities.environment_vars import EnvironmentVars


class IntegrationTestSuite:
    """Runs Tests against an active instance"""

    def __init__(self):
        pass

    def test(self, app_api_domain: str | None = None):
        """Run a full suite of integration tests"""
        env_vars: EnvironmentVars = EnvironmentVars()
        app_api_domain = app_api_domain or env_vars.api_domain

        if not app_api_domain:
            raise RuntimeError("APLOS_API_DOMAIN environment variable is not set.")

        app_config_test = TestAppConfiguration()
        config = app_config_test.test(app_api_domain=app_api_domain)

        tal: TestAppLogin = TestAppLogin()
        tal.test(env_vars=env_vars)
