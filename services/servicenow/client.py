import requests
import os
from dotenv import load_dotenv

load_dotenv()

class ServiceNowClient:
    def __init__(self):
        self.base_url = os.getenv("SNOW_BASE_URL")
        self.username = os.getenv("SNOW_USERNAME")
        self.password = os.getenv("SNOW_PASSWORD")

        print(f"DEBUG: (SNOW API Call) Client Initialized for {self.base_url} with user {self.username}")

    def get(self, endpoint, params=None):
        return requests.get(
            f"{self.base_url}{endpoint}",
            auth=(self.username, self.password),
            headers={"Accept": "application/json"},
            params=params,
            timeout=10,
        )

    def post(self, endpoint, payload):
        return requests.post(
            f"{self.base_url}{endpoint}",
            auth=(self.username, self.password),
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10,
        )

    def patch(self, endpoint, payload):
        return requests.patch(
            f"{self.base_url}{endpoint}",
            auth=(self.username, self.password),
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10,
        )
