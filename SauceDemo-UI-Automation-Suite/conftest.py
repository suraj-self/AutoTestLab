"""Pytest fixtures for SauceDemo UI tests, with logging configured.

This module configures an `execution.log` file in the suite root for
observability and provides the `browser` fixture used by tests.
"""

import logging
import sys
from pathlib import Path

import pytest
from utils.browser import get_driver

# Configure logging for UI tests: write to `SauceDemo-UI-Automation-Suite/execution.log`
_ROOT = Path(__file__).resolve().parent
_LOG_PATH = _ROOT / "execution.log"
_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("saucedemo")
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s")
    fh = logging.FileHandler(str(_LOG_PATH), encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)


@pytest.fixture
def browser():
    """Set up and tear down a WebDriver instance.

    Yields the WebDriver instance and ensures `driver.quit()` is called
    even if the test fails. Logs all lifecycle events for observability.

    Yields:
        WebDriver: Chrome WebDriver instance
    """

    logger.info("=" * 60)
    logger.info("Starting browser fixture and creating WebDriver")
    logger.info("=" * 60)
    try:
        driver = get_driver()
        logger.info("WebDriver initialized successfully")
        yield driver
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}", exc_info=True)
        raise
    finally:
        logger.info("Quitting WebDriver")
        try:
            driver.quit()
            logger.info("WebDriver closed successfully")
        except Exception as e:
            logger.error(f"Error while quitting WebDriver: {e}", exc_info=True)
        logger.info("=" * 60)
