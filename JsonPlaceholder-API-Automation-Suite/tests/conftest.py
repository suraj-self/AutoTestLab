import json
import logging

import pytest

logging.basicConfig(
    filename="execution.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# fixture for user APIs output validation
@pytest.fixture
def user_schema():
    with open("resource/user_schema.json") as schema_file:
        schema = json.load(schema_file)
    yield schema
    schema.clear()


# fixture for user APIs output validation
@pytest.fixture
def post_schema():
    with open("resource/post_schema.json") as schema_file:
        schema = json.load(schema_file)
    yield schema
    schema.clear()


# fixture for user APIs output validation
@pytest.fixture
def comment_schema():
    with open("resource/comment_schema.json") as schema_file:
        schema = json.load(schema_file)
    yield schema
    schema.clear()
