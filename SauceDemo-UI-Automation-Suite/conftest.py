"""Pytest fixtures for SauceDemo UI tests, with logging configured.

This module configures an `execution.log` file in the suite root for
observability and provides the `browser` fixture used by tests.
"""
from pathlib import Path
import logging
import sys
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

    Yields the WebDriver instance and ensures `driver.quit()` is called.
    """

    logger.info("Starting browser fixture and creating WebDriver")
    driver = get_driver()
    try:
        yield driver
    finally:
        logger.info("Quitting WebDriver")
        driver.quit()
