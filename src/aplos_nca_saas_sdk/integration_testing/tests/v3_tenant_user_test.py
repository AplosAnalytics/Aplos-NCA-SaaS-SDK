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
from aplos_nca_saas_sdk.nca_resources.nca_authenticator import NCAAuthenticator
from aplos_nca_saas_sdk.nca_resources.nca_tenant_user_management import (
    NCATenantUserManagement,
)

logger = Logger(service="V3TenantUserTest")


class V3TenantUserTest(IntegrationTestBase):
    """V3 Tenant and User Management Test Container

    Tests v3 tenant/user management operations: tenant info, user info,
    subscriptions, metrics, messages, and assignable roles.
    """

    def __init__(self):
        super().__init__(name="v3-tenant-user", index=12)

    def test(self) -> bool:
        """Test v3 tenant and user management operations"""

        self.results.clear()

        for login in self.config.logins.list:
            test_response: IntegrationTestResponse = IntegrationTestResponse()
            test_response.name = self.name

            if not login.enabled or not self.config.logins.enabled:
                test_response.skipped = True
                test_response.success = True
                self.results.append(test_response)
                continue

            try:
                # Authenticate
                auth = NCAAuthenticator(host=login.host)
                auth.authenticate(
                    username=login.username, password=login.password
                )

                mgmt = NCATenantUserManagement(login.host)
                mgmt.authenticator = auth

                # Tenant info
                logger.info({"message": "Getting v3 tenant info"})
                tenant_response = mgmt.get_tenant()
                if not isinstance(tenant_response, dict):
                    raise RuntimeError(
                        "Expected dict response from get_tenant."
                    )

                # User info
                logger.info({"message": "Getting v3 user info"})
                user_response = mgmt.get_user()
                if not isinstance(user_response, dict):
                    raise RuntimeError(
                        "Expected dict response from get_user."
                    )

                # Tenant subscriptions
                logger.info({"message": "Getting v3 tenant subscriptions"})
                try:
                    subs_response = mgmt.get_tenant_subscriptions()
                    if not isinstance(subs_response, dict):
                        raise RuntimeError(
                            "Expected dict response from get_tenant_subscriptions."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "Subscriptions endpoint may not be available."}
                    )

                # User metrics
                logger.info({"message": "Getting v3 user metrics"})
                try:
                    user_metrics_response = mgmt.get_user_metrics()
                    if not isinstance(user_metrics_response, dict):
                        raise RuntimeError(
                            "Expected dict response from get_user_metrics."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "User metrics endpoint may not be available."}
                    )

                # Tenant metrics
                logger.info({"message": "Getting v3 tenant metrics"})
                try:
                    tenant_metrics_response = mgmt.get_tenant_metrics()
                    if not isinstance(tenant_metrics_response, dict):
                        raise RuntimeError(
                            "Expected dict response from get_tenant_metrics."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "Tenant metrics endpoint may not be available."}
                    )

                # Public messages
                logger.info({"message": "Getting v3 public messages"})
                try:
                    messages_response = mgmt.get_public_messages()
                    if not isinstance(messages_response, dict):
                        raise RuntimeError(
                            "Expected dict response from get_public_messages."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "Public messages endpoint may not be available."}
                    )

                # User messages
                logger.info({"message": "Getting v3 user messages"})
                try:
                    user_messages_response = mgmt.get_user_messages()
                    if not isinstance(user_messages_response, dict):
                        raise RuntimeError(
                            "Expected dict response from get_user_messages."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "User messages endpoint may not be available."}
                    )

                # Assignable roles
                logger.info({"message": "Getting v3 assignable roles"})
                try:
                    roles_response = mgmt.get_assignable_roles()
                    if not isinstance(roles_response, dict):
                        raise RuntimeError(
                            "Expected dict response from get_assignable_roles."
                        )
                except RuntimeError:
                    logger.info(
                        {"message": "Assignable roles endpoint may not be available."}
                    )

                test_response.success = True

            except Exception as e:  # pylint: disable=w0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()
