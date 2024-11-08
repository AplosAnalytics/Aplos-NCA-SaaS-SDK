"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA

No part of this publication may be reproduced, stored or transmitted,
in any form or by any means (electronic, mechanical, photocopying,
recording or otherwise) without prior written permission from Aplos Analytices, Inc.
"""

import os
from aplos_nca_saas_toolkit.utilities.environment_services import EnvironmentServices
from aplos_nca_saas_toolkit.integration_testing.integration_test_suite import (
    IntegrationTestSuite,
)


def main():
    """Run the tests"""

    evs: EnvironmentServices = EnvironmentServices()
    env_file = os.getenv("ENV_FILE")
    if env_file:
        # if we have an environment file defined, let's load it
        evs.load_environment(starting_path=__file__, file_name=env_file)

    its: IntegrationTestSuite = IntegrationTestSuite()
    its.test()


if __name__ == "__main__":
    main()
