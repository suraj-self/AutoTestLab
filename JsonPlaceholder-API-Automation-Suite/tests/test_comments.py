import pytest
import requests
from config import BASE_URL, HEADERS
from jsonschema import validate, ValidationError
import logging

logger = logging.getLogger(__name__)

class TestCommentsAPI:
    @pytest.mark.comments_tests
    def test_get_comments(self, comment_schema):
        """
        Test fetching all comments from the API.

        This test performs the following:
        - Sends a GET request to the API endpoint to retrieve all comments.
        - Validates the response status code is 200.
        - Ensures the response contains a list of comments.
        - Verifies the total number of comments matches the expected count (500).
        - Validates each comment object against the provided JSON schema.

        Logs detailed information about the response and validation process.
        Handles exceptions for HTTP requests, schema validation, and unexpected errors.

        Args:
            comment_schema (dict): JSON schema for validating each comment object.
        """
        logger.info("Starting test: test_get_comments")
        try:
            # Send the GET request to fetch comments
            response = requests.get(url=f"{BASE_URL}comments", headers=HEADERS)
            logger.info(f"GET {BASE_URL}comments - Status Code: {response.status_code}")
            assert response.status_code == 200

            # Parse and validate response
            response_data = response.json()
            assert isinstance(response_data, list)
            assert len(response_data) == 500
            logger.info(f"Response contains {len(response_data)} comments")

            # Validate each comment data using comment schema
            for item in response_data:
                validate(instance=item, schema=comment_schema)
            logger.info("All comments validated successfully against the schema")

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
            logger.info("Finished test: test_get_comments")
