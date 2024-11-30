import pytest
import requests
from config import BASE_URL, HEADERS
from jsonschema import validate, ValidationError
import logging

logger = logging.getLogger(__name__)

class TestUsersAPI:
    @pytest.mark.users_tests
    def test_fetch_all_users(self, user_schema):
        """
        Test fetching all users from the API.

        This test sends a GET request to fetch all users from the API endpoint.
        It validates the following:
        - Response status code is 200.
        - Response is a list of users.
        - The number of users matches the expected count.
        - Each user object adheres to the defined JSON schema.

        Logs details about the response and validates against schema.
        Handles exceptions related to HTTP requests, schema validation, 
        and unexpected errors.

        Args:
            user_schema (dict): The JSON schema used to validate user data.
        """
        logger.info("Starting test: test_fetch_all_users")
        try:
            # Send a GET request to fetch all users
            response = requests.get(url=f"{BASE_URL}users", headers=HEADERS)
            logger.info(f"GET {BASE_URL}users - Status Code: {response.status_code}")
            assert response.status_code == 200

            # Validate the response data
            response_data = response.json()
            assert isinstance(response_data, list)
            assert len(response_data) == 10
            logger.info(f"Response contains {len(response_data)} users")

            # Validate each user against the JSON schema
            for item in response_data:
                validate(instance=item, schema=user_schema)
            logger.info("All users validated successfully against the schema")

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request failed: {str(e)}")
            pytest.fail(f"HTTP request failed: {str(e)}")

        except ValidationError as e:
            logger.error(f"Schema validation failed: {e.message}")
            pytest.fail(f"Validation failed: {e.message}")

        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            pytest.fail(f"Unexpected error: {str(e)}")

        finally:
            logger.info("Finished test: test_fetch_all_users")

    @pytest.mark.users_tests
    def test_fetch_single_user(self, user_schema):
        """
        Test fetching a single user from the API.

        This test sends a GET request to fetch a user with a specific ID.
        It validates the following:
        - Response status code is 200.
        - Response is a dictionary representing a single user.
        - The user object contains the expected keys (e.g., 'id').
        - The user object adheres to the defined JSON schema.

        Logs details about the response and validates against schema.
        Handles exceptions related to HTTP requests, schema validation, 
        and unexpected errors.

        Args:
            user_schema (dict): The JSON schema used to validate user data.
        """
        logger.info("Starting test: test_fetch_single_user")
        try:
            # Send a GET request to fetch a single user
            response = requests.get(url=f"{BASE_URL}users/1", headers=HEADERS)
            logger.info(f"GET {BASE_URL}users/1 - Status Code: {response.status_code}")
            assert response.status_code == 200

            # Validate the response data
            user_data = response.json()
            assert isinstance(user_data, dict)
            assert "id" in user_data
            logger.info(f"User data contains expected keys: {user_data.keys()}")

            # Validate the user data against the JSON schema
            validate(instance=user_data, schema=user_schema)
            logger.info("User data validated successfully against the schema")

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request failed: {str(e)}")
            pytest.fail(f"HTTP request failed: {str(e)}")

        except ValidationError as e:
            logger.error(f"Schema validation failed: {e.message}")
            pytest.fail(f"Validation failed: {e.message}")

        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            pytest.fail(f"Unexpected error: {str(e)}")

        finally:
            logger.info("Finished test: test_fetch_single_user")

    @pytest.mark.users_tests
    def test_search_for_user(self, user_schema):
        """
        Test searching for a user by query parameter.

        This test sends a GET request to search for a user with a specific query parameter.
        It validates the following:
        - Response status code is 200.
        - Response is a list containing exactly one user.
        - The user object adheres to the defined JSON schema.

        Logs details about the response and validates against schema.
        Handles exceptions related to HTTP requests, schema validation, 
        and unexpected errors.

        Args:
            user_schema (dict): The JSON schema used to validate user data.
        """
        logger.info("Starting test: test_search_for_user")
        try:
            # Send a GET request to search for a user
            response = requests.get(url=f"{BASE_URL}/users?id=2", headers=HEADERS)
            logger.info(f"GET {BASE_URL}/users?id=2 - Status Code: {response.status_code}")
            assert response.status_code == 200

            # Validate the search response data
            data = response.json()
            assert len(data) == 1
            assert isinstance(data, list)
            logger.info(f"Search result contains {len(data)} user(s)")

            # Validate the user data against the JSON schema
            response_data = data[0]
            validate(instance=response_data, schema=user_schema)
            logger.info("User search result validated successfully against the schema")

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request failed: {str(e)}")
            pytest.fail(f"HTTP request failed: {str(e)}")

        except ValidationError as e:
            logger.error(f"Schema validation failed: {e.message}")
            pytest.fail(f"Validation failed: {e.message}")

        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            pytest.fail(f"Unexpected error: {str(e)}")

        finally:
            logger.info("Finished test: test_search_for_user")
