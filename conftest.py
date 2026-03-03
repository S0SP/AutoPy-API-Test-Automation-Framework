import json
import logging
import os
import pytest
from utils.api_client import APIClient
from utils.logger import setup_logger
from config.settings import Config

setup_logger()
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────
# Session-scoped: one client for whole run
# ──────────────────────────────────────────

@pytest.fixture(scope="session")
def api_client() -> APIClient:
    """Unauthenticated API client (shared across session)."""
    logger.info("⚙️  Creating unauthenticated API client")
    client = APIClient()
    yield client
    logger.info("✅ Session complete — API client released")


@pytest.fixture(scope="session")
def auth_token(api_client: APIClient) -> str:
    """Login once, reuse token for entire test session."""
    logger.info("🔐 Fetching auth token")
    payload = {"email": Config.EMAIL, "password": Config.PASSWORD}
    response = api_client.post("/login", payload)
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["token"]
    logger.info(f"🔑 Token acquired: {token}")
    return token


@pytest.fixture(scope="session")
def auth_client(auth_token: str) -> APIClient:
    """Authenticated API client with Bearer token."""
    client = APIClient(token=auth_token)
    return client


# ──────────────────────────────────────────
# Data fixtures
# ──────────────────────────────────────────

@pytest.fixture(scope="session")
def users_data() -> dict:
    """Load user test data from JSON file."""
    data_path = os.path.join(os.path.dirname(__file__), "data", "users.json")
    with open(data_path) as f:
        return json.load(f)


@pytest.fixture(scope="function")
def created_user_id(api_client: APIClient, users_data: dict) -> int:
    """Create a user before test, delete after — clean teardown."""
    payload = users_data["create_users"][0]
    response = api_client.post("/users", payload)
    assert response.status_code == 201
    user_id = response.json()["id"]
    logger.info(f"🆕 Created user id={user_id} for test")

    yield user_id

    # Teardown: delete created user
    api_client.delete(f"/users/{user_id}")
    logger.info(f"🗑️  Deleted user id={user_id} after test")


# ──────────────────────────────────────────
# Pytest hooks
# ──────────────────────────────────────────

def pytest_configure(config):
    os.makedirs("reports", exist_ok=True)


def pytest_runtest_logreport(report):
    if report.when == "call":
        if report.passed:
            logger.info(f"✅ PASSED: {report.nodeid}")
        elif report.failed:
            logger.error(f"❌ FAILED: {report.nodeid}")
