import requests
from aplos_nca_saas_sdk.nca_resources.nca_endpoints import NCAEndpoints


class NCAAppConfiguration:
    def __init__(self, domain: str):
        self.endpoints: NCAEndpoints = NCAEndpoints(domain=domain)

    def get(self) -> requests.Response:
        """Executes a HTTP Get request"""

        url = self.endpoints.app_configuration()
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            print(f"App configuration url is working. {url}")
            print(f"App configuration: {response.json()}")
        else:
            print(
                f"App configuration url is not working. Status code: {response.status_code}"
            )
            raise RuntimeError("App configuration url is not working.")

        return response
