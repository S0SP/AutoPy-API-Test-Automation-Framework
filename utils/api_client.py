import logging
import requests
from config.settings import Config

logger = logging.getLogger(__name__)


class APIClient:
    """
    Reusable HTTP client wrapper for all API interactions.
    Centralizes request handling, logging, and error management.
    """

    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = base_url or Config.base_api_url()
        self.session = requests.Session()
        self.timeout = Config.REQUEST_TIMEOUT

        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

        # Required by reqres.in — API key sent on every request
        api_key = Config.API_KEY
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if api_key:
            headers["x-api-key"] = api_key

        self.session.headers.update(headers)

    def set_auth_token(self, token: str):
        """Set or update auth token on session."""
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info("Auth token set on session.")

    def get(self, endpoint: str, params: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url} | params={params}")
        response = self.session.get(url, params=params, timeout=self.timeout)
        self._log_response(response)
        return response

    def post(self, endpoint: str, payload: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url} | payload={payload}")
        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._log_response(response)
        return response

    def put(self, endpoint: str, payload: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url} | payload={payload}")
        response = self.session.put(url, json=payload, timeout=self.timeout)
        self._log_response(response)
        return response

    def patch(self, endpoint: str, payload: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PATCH {url} | payload={payload}")
        response = self.session.patch(url, json=payload, timeout=self.timeout)
        self._log_response(response)
        return response

    def delete(self, endpoint: str) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        response = self.session.delete(url, timeout=self.timeout)
        self._log_response(response)
        return response

    def _log_response(self, response: requests.Response):
        logger.info(
            f"Response: status={response.status_code} "
            f"time={response.elapsed.total_seconds():.3f}s"
        )
        if response.content:
            try:
                logger.debug(f"Body: {response.json()}")
            except Exception:
                logger.debug(f"Body (raw): {response.text[:500]}")
