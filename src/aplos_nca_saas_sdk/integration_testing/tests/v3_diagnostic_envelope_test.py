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
from aplos_nca_saas_sdk.nca_resources.v3.diagnostic_envelope import (
    DiagnosticEnvelopeHandler,
)

logger = Logger(service="V3DiagnosticEnvelopeTest")


class V3DiagnosticEnvelopeTest(IntegrationTestBase):
    """V3 Diagnostic Envelope Test Container

    Verifies that the diagnostic envelope is correctly unwrapped for
    live v3 responses. Uses a simple v3 endpoint call and checks that
    the response has been unwrapped (no envelope keys at top level)
    and that diagnostics metadata is accessible.
    """

    def __init__(self):
        super().__init__(name="v3-diagnostic-envelope", index=13)

    def test(self) -> bool:
        """Test diagnostic envelope unwrapping on live v3 responses"""

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

                # Make a v3 call that returns an envelope-wrapped response.
                # get_user() calls the v3 user endpoint and processes the
                # response through the diagnostic envelope handler.
                logger.info(
                    {"message": "Calling v3 user endpoint to test envelope unwrap"}
                )
                response = mgmt.get_user()

                # The response should be the unwrapped data payload.
                # It should NOT contain the top-level envelope keys
                # (statusCode, timestamp, success) since those belong
                # to the envelope wrapper, not the inner data.
                if not isinstance(response, dict):
                    raise RuntimeError(
                        "Expected dict response from v3 user endpoint."
                    )

                # Verify envelope was unwrapped: the top-level response
                # should not look like a raw envelope.
                is_still_envelope = DiagnosticEnvelopeHandler.is_envelope(response)
                if is_still_envelope:
                    raise RuntimeError(
                        "Response still appears to be a raw diagnostic envelope. "
                        "Envelope unwrapping may not be working correctly."
                    )

                # Verify diagnostics metadata is accessible via the
                # _diagnostics key injected by the envelope handler.
                diagnostics = response.get("_diagnostics")
                if diagnostics is None:
                    raise RuntimeError(
                        "Expected _diagnostics key in unwrapped v3 response. "
                        "Envelope handler may not be attaching diagnostics."
                    )

                if not isinstance(diagnostics, dict):
                    raise RuntimeError(
                        "Expected _diagnostics to be a dict."
                    )

                logger.info(
                    {
                        "message": "Diagnostic envelope correctly unwrapped",
                        "diagnostics_keys": list(diagnostics.keys()),
                    }
                )

                test_response.success = True

            except Exception as e:  # pylint: disable=w0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()
