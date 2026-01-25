"""Pytest fixtures for JSONPlaceholder API tests with comprehensive logging."""

import json
import logging
from pathlib import Path

import pytest

# Configure logging for API tests
_ROOT = Path(__file__).resolve().parent.parent
_LOG_PATH = _ROOT / "execution.log"
_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("jsonplaceholder_api")
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)s [%(funcName)s]: %(message)s"
    )
    fh = logging.FileHandler(str(_LOG_PATH), encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)


@pytest.fixture
def user_schema():
    """Load and validate user schema JSON fixture."""
    logger.info("Loading user_schema fixture")
    try:
        schema_path = Path("resource/user_schema.json")
        with open(schema_path, encoding="utf-8") as schema_file:
            schema = json.load(schema_file)
        logger.debug(f"Loaded user schema from {schema_path}")
        yield schema
    except FileNotFoundError as e:
        logger.error(f"User schema file not found: {e}")
        pytest.fail(f"Schema file missing: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in user schema: {e}")
        pytest.fail(f"Invalid schema JSON: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading user schema: {e}")
        pytest.fail(f"Schema loading failed: {e}")
    finally:
        logger.debug("Cleaning up user_schema fixture")
        schema.clear()


@pytest.fixture
def post_schema():
    """Load and validate post schema JSON fixture."""
    logger.info("Loading post_schema fixture")
    try:
        schema_path = Path("resource/post_schema.json")
        with open(schema_path, encoding="utf-8") as schema_file:
            schema = json.load(schema_file)
        logger.debug(f"Loaded post schema from {schema_path}")
        yield schema
    except FileNotFoundError as e:
        logger.error(f"Post schema file not found: {e}")
        pytest.fail(f"Schema file missing: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in post schema: {e}")
        pytest.fail(f"Invalid schema JSON: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading post schema: {e}")
        pytest.fail(f"Schema loading failed: {e}")
    finally:
        logger.debug("Cleaning up post_schema fixture")
        schema.clear()


@pytest.fixture
def comment_schema():
    """Load and validate comment schema JSON fixture."""
    logger.info("Loading comment_schema fixture")
    try:
        schema_path = Path("resource/comment_schema.json")
        with open(schema_path, encoding="utf-8") as schema_file:
            schema = json.load(schema_file)
        logger.debug(f"Loaded comment schema from {schema_path}")
        yield schema
    except FileNotFoundError as e:
        logger.error(f"Comment schema file not found: {e}")
        pytest.fail(f"Schema file missing: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in comment schema: {e}")
        pytest.fail(f"Invalid schema JSON: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading comment schema: {e}")
        pytest.fail(f"Schema loading failed: {e}")
    finally:
        logger.debug("Cleaning up comment_schema fixture")
        schema.clear()
