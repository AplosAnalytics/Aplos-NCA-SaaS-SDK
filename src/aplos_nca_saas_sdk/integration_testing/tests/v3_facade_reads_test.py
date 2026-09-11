"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from aws_lambda_powertools import Logger

from aplos_nca_saas_sdk.client import AplosClient, AplosApiError
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_response import (
    IntegrationTestResponse,
)

logger = Logger(service="V3FacadeReadsTest")


class V3FacadeReadsTest(IntegrationTestBase):
    """Read-only coverage via the AplosClient facade (NE-1849 / NE-1850).

    Exercises documented endpoints that previously had no integration coverage,
    through the new typed facade rather than the legacy nca_resources classes:
      - workflow: history, root, lineage
      - tenants: list, get
      - users:   list

    All calls are read-only and safe to run against a live tenant. Each
    endpoint is tolerant of "not available in this environment" style errors
    (logged, not failed) so the suite is portable across deployments; only an
    unexpected failure marks the test as an error.
    """

    def __init__(self):
        super().__init__(name="v3-facade-reads", index=14)

    def test(self) -> bool:
        self.results.clear()

        for login in self.config.logins.list:
            test_response = IntegrationTestResponse()
            test_response.name = self.name

            if not login.enabled or not self.config.logins.enabled:
                test_response.skipped = True
                test_response.success = True
                self.results.append(test_response)
                continue

            try:
                client = AplosClient(host=login.host)
                client.login(username=login.username, password=login.password)

                # --- workflow reads -------------------------------------------------
                # History is the anchor: if there is at least one execution, use
                # it to exercise status/root/lineage; otherwise skip those.
                logger.info({"message": "facade: workflow.history"})
                history = client.workflow.history()
                executions = getattr(history, "executions", None) or []

                if executions:
                    exec_id = executions[0].id
                    logger.info({"message": "facade: workflow.status", "id": exec_id})
                    client.workflow.status(exec_id)
                    logger.info({"message": "facade: workflow.root", "id": exec_id})
                    client.workflow.root(exec_id)
                    logger.info({"message": "facade: workflow.lineage", "id": exec_id})
                    client.workflow.lineage(exec_id)
                else:
                    logger.info(
                        {"message": "no executions; skipping status/root/lineage"}
                    )

                # --- tenant reads ---------------------------------------------------
                logger.info({"message": "facade: tenants.get"})
                client.tenants.get()

                # tenants.list is platform-admin only; tolerate a permission error.
                logger.info({"message": "facade: tenants.list"})
                try:
                    client.tenants.list()
                except AplosApiError as e:
                    logger.info(
                        {
                            "message": "tenants.list not permitted/available",
                            "code": e.code,
                        }
                    )

                # --- user reads -----------------------------------------------------
                logger.info({"message": "facade: users.list"})
                try:
                    client.users.list()
                except AplosApiError as e:
                    logger.info(
                        {
                            "message": "users.list not permitted/available",
                            "code": e.code,
                        }
                    )

                # --- subscription reads --------------------------------------------
                logger.info({"message": "facade: subscriptions.active"})
                try:
                    client.subscriptions.active()
                except AplosApiError as e:
                    logger.info(
                        {"message": "active subscription not available", "code": e.code}
                    )

                test_response.success = True

            except Exception as e:  # pylint: disable=broad-except
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()
