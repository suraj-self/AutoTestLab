import pytest
import requests
from config import BASE_URL, HEADERS
from jsonschema import validate, ValidationError
import logging

logger = logging.getLogger(__name__)

class TestPostAPI:
    @pytest.mark.posts_tests
    def test_get_posts(self, post_schema):
        """
        Test fetching all posts from the API.

        This test performs the following:
        - Sends a GET request to the API endpoint to retrieve all posts.
        - Validates the response status code is 200.
        - Ensures the response contains a list of posts.
        - Verifies the total number of posts matches the expected count (100).
        - Validates each post object against the provided JSON schema.

        Logs detailed information about the response and validation process.
        Handles exceptions for HTTP requests, schema validation, and unexpected errors.

        Args:
            post_schema (dict): JSON schema for validating each post.
        """
        logger.info("Starting test: test_get_posts")
        try:
            # Sending GET request
            response = requests.get(url=f"{BASE_URL}posts", headers=HEADERS)
            logger.info(f"GET {BASE_URL}posts - Status Code: {response.status_code}")
            assert response.status_code == 200
            
            # Parsing and validating response
            response_data = response.json()
            assert isinstance(response_data, list)
            logger.info(f"Response contains {len(response_data)} items")
            assert len(response_data) == 100

            # Validate each post data using post schema
            for item in response_data:
                validate(instance=item, schema=post_schema)
            logger.info("All items validated successfully against the schema")
        
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
            logger.info("Finished test: test_get_posts")

    @pytest.mark.posts_tests
    def test_get_post(self, post_schema):
        """
        Test fetching a single post from the API.

        This test performs the following:
        - Sends a GET request to the API endpoint to retrieve a specific post by ID.
        - Validates the response status code is 200.
        - Ensures the response is a dictionary representing a single post.
        - Verifies the ID of the retrieved post matches the expected ID (2).
        - Validates the post object against the provided JSON schema.

        Logs detailed information about the response and validation process.
        Handles exceptions for HTTP requests, schema validation, and unexpected errors.

        Args:
            post_schema (dict): JSON schema for validating the post object.
        """
        logger.info("Starting test: test_get_post")
        try:
            # Sending GET request for a specific post
            response = requests.get(url=f"{BASE_URL}posts/2", headers=HEADERS)
            logger.info(f"GET {BASE_URL}posts/2 - Status Code: {response.status_code}")
            assert response.status_code == 200

            # Parsing and validating response
            response_data = response.json()
            assert isinstance(response_data, dict)
            assert response_data["id"] == 2
            logger.info(f"Response data ID: {response_data['id']} matches the expected value")

            # Validate post data using post schema
            validate(instance=response_data, schema=post_schema)
            logger.info("Post data validated successfully against the schema")
        
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
            logger.info("Finished test: test_get_post")
