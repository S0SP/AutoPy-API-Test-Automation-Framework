import logging
import pytest
from utils.api_client import APIClient
from utils.assertions import Assertions
from data.schemas import LOGIN_SCHEMA
from config.settings import Config

logger = logging.getLogger(__name__)


class TestAuthentication:

    @pytest.mark.smoke
    @pytest.mark.auth
    def test_login_valid_credentials(self, api_client: APIClient):
        """POST /login with valid credentials returns token."""
        payload = {"email": Config.EMAIL, "password": Config.PASSWORD}
        response = api_client.post("/login", payload)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_schema(response, LOGIN_SCHEMA)
        token = response.json().get("token")
        assert token and len(token) > 0, "Token should not be empty"
        logger.info(f"✅ Login successful, token received: {token}")

    @pytest.mark.auth
    def test_login_missing_password(self, api_client: APIClient):
        """POST /login without password returns 400."""
        payload = {"email": Config.EMAIL}
        response = api_client.post("/login", payload)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_key_in_response(response, "error")
        logger.info("✅ Missing password correctly returns 400")

    @pytest.mark.auth
    def test_login_missing_email(self, api_client: APIClient):
        """POST /login without email returns 400."""
        payload = {"password": Config.PASSWORD}
        response = api_client.post("/login", payload)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_key_in_response(response, "error")

    @pytest.mark.auth
    def test_register_valid_credentials(self, api_client: APIClient):
        """POST /register with valid credentials returns token."""
        payload = {
            "email": Config.REGISTER_EMAIL,
            "password": Config.REGISTER_PASSWORD,
        }
        response = api_client.post("/register", payload)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_key_in_response(response, "token")
        Assertions.assert_key_in_response(response, "id")

    @pytest.mark.auth
    def test_register_missing_password(self, api_client: APIClient):
        """POST /register without password returns error."""
        payload = {"email": "test@example.com"}
        response = api_client.post("/register", payload)
        Assertions.assert_status_code(response, 400)
        error_msg = response.json().get("error", "")
        assert "password" in error_msg.lower() or len(error_msg) > 0
        logger.info(f"✅ Registration without password returns 400: {error_msg}")

    @pytest.mark.auth
    def test_authenticated_request(self, auth_client: APIClient):
        """Authenticated client can access user endpoint successfully."""
        response = auth_client.get("/users/1")
        Assertions.assert_status_code(response, 200)
        logger.info("✅ Authenticated request succeeded")
