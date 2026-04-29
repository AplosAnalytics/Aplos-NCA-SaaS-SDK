"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Any, Dict

import requests

from aplos_nca_saas_sdk.nca_resources.nca_endpoints import NCAEndpoints


class NCAAppConfiguration:
    """
    NCA Application Configuration



    "idp": {
        "Auth": {
        "Cognito": {
            "region": "<region>",
            "userPoolId": "<user-pool-id>",
            "userPoolClientId": "<user-pool-client-id>",
            "authenticationFlowType": "<auth-flow-type>"
        }
        }
    },

    """

    def __init__(self, host: str, *, api_version: str | None = None):
        self.__api_version: str = api_version or "v1"
        self.__endpoints: NCAEndpoints = NCAEndpoints(host=host)
        self.__host: str = host
        self.__response: requests.Response | None = None

    @property
    def config_url(self) -> str:
        """Return the configuration endpoint URL.

        For v3 this is ``/v3/app/configuration``; for v1 (or any other
        version) the existing :pyattr:`NCAEndpoints.app_configuration`
        URL is returned.
        """
        if self.__api_version == "v3":
            return f"https://{self.__host}/v3/app/configuration"
        return self.__endpoints.app_configuration

    def get(self) -> requests.Response:
        """Executes a HTTP Get request"""

        if self.__response is not None:
            return self.__response

        url = self.config_url
        self.__response = requests.get(url, timeout=30)
        if self.__response.status_code != 200:
            raise RuntimeError(
                f"App configuration endpoint failed: {url} "
                f"(status {self.__response.status_code})"
            )

        return self.__response

    def get_api_routing(self) -> Dict[str, Any]:
        """Extract the ``api_routing`` map from the configuration response.

        Returns an empty dict when the key is absent.
        """
        data: Dict[str, Any] = self.get().json()
        return data.get("api_routing", {})

    @property
    def cognito_client_id(self) -> str:
        """Returns the cognito client id"""
        data: Dict[str, Any] = self.get().json()
        cognito_client_id = (
            data.get("idp", {})
            .get("Auth", {})
            .get("Cognito", {})
            .get("userPoolClientId")
        )
        return cognito_client_id

    @property
    def cognito_region(self) -> str:
        """Returns the cognito region"""
        data: Dict[str, Any] = self.get().json()
        cognito_client_id = (
            data.get("idp", {}).get("Auth", {}).get("Cognito", {}).get("region")
        )
        return cognito_client_id
