import logging
import pytest
from utils.api_client import APIClient
from utils.assertions import Assertions
from data.schemas import USER_SCHEMA, USERS_LIST_SCHEMA, CREATE_USER_SCHEMA

logger = logging.getLogger(__name__)


class TestGetUsers:

    @pytest.mark.smoke
    @pytest.mark.users
    def test_get_users_list_returns_200(self, api_client: APIClient):
        """GET /users returns status 200 with user list."""
        response = api_client.get("/users", params={"page": 1})
        Assertions.assert_status_code(response, 200)
        Assertions.assert_list_not_empty(response, "data")

    @pytest.mark.users
    def test_get_users_list_schema_valid(self, api_client: APIClient):
        """GET /users response matches expected JSON schema."""
        response = api_client.get("/users")
        Assertions.assert_status_code(response, 200)
        Assertions.assert_schema(response, USERS_LIST_SCHEMA)

    @pytest.mark.users
    def test_get_users_pagination(self, api_client: APIClient):
        """Pagination returns correct page number."""
        response = api_client.get("/users", params={"page": 2})
        Assertions.assert_status_code(response, 200)
        Assertions.assert_value_equals(response, "page", 2)

    @pytest.mark.users
    @pytest.mark.parametrize("user_id, expected_first, expected_last", [
        (1, "George", "Bluth"),
        (2, "Janet", "Weaver"),
        (3, "Emma", "Wong"),
    ])
    def test_get_single_user_parametrized(
        self, api_client: APIClient, user_id, expected_first, expected_last
    ):
        """GET /users/{id} returns correct user data (parametrized)."""
        response = api_client.get(f"/users/{user_id}")
        Assertions.assert_status_code(response, 200)
        Assertions.assert_schema(response, USER_SCHEMA)
        body = response.json()["data"]
        assert body["first_name"] == expected_first, (
            f"Expected first_name={expected_first}, got {body['first_name']}"
        )
        assert body["last_name"] == expected_last
        logger.info(f"✅ User {user_id}: {expected_first} {expected_last} verified")

    @pytest.mark.users
    def test_get_nonexistent_user_returns_404(self, api_client: APIClient, users_data: dict):
        """GET /users/{invalid_id} returns 404 Not Found."""
        response = api_client.get(f"/users/{users_data['invalid_user_id']}")
        Assertions.assert_status_code(response, 404)

    @pytest.mark.users
    def test_get_user_response_time(self, api_client: APIClient):
        """GET /users response must complete within 3 seconds."""
        response = api_client.get("/users/1")
        Assertions.assert_status_code(response, 200)
        Assertions.assert_response_time(response, max_seconds=3.0)


class TestCreateUser:

    @pytest.mark.users
    @pytest.mark.parametrize("user", [
        {"name": "Alice Johnson", "job": "QA Engineer"},
        {"name": "Bob Smith", "job": "DevOps Lead"},
        {"name": "Carol White", "job": "Backend Developer"},
    ])
    def test_create_user_parametrized(self, api_client: APIClient, user: dict):
        """POST /users creates user and returns 201 with schema (data-driven)."""
        response = api_client.post("/users", user)
        Assertions.assert_status_code(response, 201)
        Assertions.assert_schema(response, CREATE_USER_SCHEMA)
        Assertions.assert_value_equals(response, "name", user["name"])
        Assertions.assert_value_equals(response, "job", user["job"])
        logger.info(f"✅ Created user: {user['name']} ({user['job']})")

    @pytest.mark.users
    def test_create_user_returns_id(self, api_client: APIClient):
        """POST /users response contains a valid id field."""
        payload = {"name": "Test User", "job": "Tester"}
        response = api_client.post("/users", payload)
        Assertions.assert_status_code(response, 201)
        Assertions.assert_key_in_response(response, "id")
        Assertions.assert_key_in_response(response, "createdAt")


class TestUpdateUser:

    @pytest.mark.users
    def test_put_update_user(self, api_client: APIClient, users_data: dict):
        """PUT /users/{id} fully updates user and returns 200."""
        payload = users_data["update_user"]
        response = api_client.put("/users/2", payload)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_value_equals(response, "name", payload["name"])
        Assertions.assert_value_equals(response, "job", payload["job"])

    @pytest.mark.users
    def test_patch_update_user(self, api_client: APIClient):
        """PATCH /users/{id} partially updates user and returns 200."""
        payload = {"job": "Lead Automation Engineer"}
        response = api_client.patch("/users/2", payload)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_value_equals(response, "job", payload["job"])
        Assertions.assert_key_in_response(response, "updatedAt")


class TestDeleteUser:

    @pytest.mark.users
    def test_delete_user_returns_204(self, api_client: APIClient):
        """DELETE /users/{id} returns 204 No Content."""
        response = api_client.delete("/users/2")
        Assertions.assert_status_code(response, 204)
        assert response.text == "", "Expected empty body on 204"
        logger.info("✅ User deleted successfully, body is empty")
