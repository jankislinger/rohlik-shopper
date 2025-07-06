from typing import Any

import requests

DEFAULT_BASE_URL = "https://www.rohlik.cz/services/frontend-service"


class RohlikSession:
    """Wrapper around request.Session."""

    def __init__(self, base_url=DEFAULT_BASE_URL):
        self._base_url = base_url
        self._session = requests.Session()

    def get(self, endpoint, params=None) -> Any:
        """Send GET request."""
        response = self._session.get(self._url(endpoint), params=params)
        response.raise_for_status()
        return response.json()

    def get_api(self, endpoint, params=None) -> Any:
        """Send GET request."""
        # TODO: fix in base URL so that we don't need two methods
        url = self._url(endpoint).replace("services/frontend-service", "api")
        response = self._session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, json=None) -> Any:
        """Send POST request."""
        response = self._session.post(self._url(endpoint), json=json)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, json=None) -> Any:
        """Send PUT request."""
        response = self._session.put(self._url(endpoint), json=json)
        response.raise_for_status()
        return response.json()

    def _url(self, endpoint: str) -> str:
        return f"{self._base_url}/{endpoint}"
