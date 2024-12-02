import requests


class TestAppConfiguration:
    """Application Configuration Tests"""

    def __init__(self):
        pass

    def test(self, app_api_domain: str) -> dict:
        """Test loading the application configuration"""
        url = f"https://{app_api_domain}/app/configuration"

        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            print(f"App configuration url is working. {url}")
            print(f"App configuration: {response.json()}")
        else:
            print(
                f"App configuration url is not working. Status code: {response.status_code}"
            )
            raise RuntimeError("App configuration url is not working.")

        return response.json()
