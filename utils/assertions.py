import logging
import jsonschema
import requests

logger = logging.getLogger(__name__)


class Assertions:
    """
    Custom assertion helpers for API test validation.
    Provides clear, descriptive error messages on failure.
    """

    @staticmethod
    def assert_status_code(response: requests.Response, expected: int):
        actual = response.status_code
        assert actual == expected, (
            f"Expected status {expected}, got {actual}. "
            f"Response: {response.text[:300]}"
        )
        logger.info(f"✅ Status code {actual} matched expected {expected}")

    @staticmethod
    def assert_response_time(response: requests.Response, max_seconds: float = 3.0):
        elapsed = response.elapsed.total_seconds()
        assert elapsed <= max_seconds, (
            f"Response took {elapsed:.3f}s, exceeded limit of {max_seconds}s"
        )
        logger.info(f"✅ Response time {elapsed:.3f}s within limit {max_seconds}s")

    @staticmethod
    def assert_key_in_response(response: requests.Response, key: str):
        body = response.json()
        assert key in body, f"Expected key '{key}' not found in response: {body}"
        logger.info(f"✅ Key '{key}' present in response")

    @staticmethod
    def assert_value_equals(response: requests.Response, key: str, expected_value):
        body = response.json()
        actual = body.get(key)
        assert actual == expected_value, (
            f"For key '{key}': expected '{expected_value}', got '{actual}'"
        )
        logger.info(f"✅ Key '{key}' = '{actual}' matches expected '{expected_value}'")

    @staticmethod
    def assert_schema(response: requests.Response, schema: dict):
        """Validate response body against a JSON Schema."""
        body = response.json()
        try:
            jsonschema.validate(instance=body, schema=schema)
            logger.info("✅ Schema validation passed")
        except jsonschema.ValidationError as e:
            raise AssertionError(f"Schema validation failed: {e.message}")

    @staticmethod
    def assert_list_not_empty(response: requests.Response, key: str = "data"):
        body = response.json()
        items = body.get(key, [])
        assert len(items) > 0, f"Expected non-empty list for key '{key}', got: {items}"
        logger.info(f"✅ List '{key}' has {len(items)} items")
