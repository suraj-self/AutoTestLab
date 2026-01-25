"""WebDriver factory for UI tests supporting local and Selenium Grid execution."""

import logging
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger("saucedemo.browser")


def get_driver():
    """Create and return a Chrome WebDriver instance.

    Supports two modes:
    1. Local: Uses local ChromeDriver with ChromeDriverManager
    2. Grid: Connects to remote Selenium Hub

    Environment Variables:
    - USE_GRID: 'true' to use Selenium Grid (default: false)
    - SELENIUM_HUB_URL: Selenium Hub URL (default: http://localhost:4444)

    Returns:
        WebDriver: Chrome WebDriver instance

    Raises:
        Exception: If driver initialization fails
    """
    logger.info("Initializing WebDriver")
    use_grid = os.getenv("USE_GRID", "false").lower() == "true"
    selenium_hub_url = os.getenv("SELENIUM_HUB_URL", "http://localhost:4444")

    try:
        if use_grid:
            logger.info(
                f"Creating remote WebDriver for Selenium Hub: {selenium_hub_url}"
            )
            return get_remote_driver(selenium_hub_url)
        logger.info("Creating local WebDriver with ChromeDriverManager")
        return get_local_driver()
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}", exc_info=True)
        raise


def get_local_driver():
    """Create a headless local Chrome WebDriver.

    Configures Chrome options for headless mode with sandbox and shm handling.
    Uses ChromeDriverManager to automatically manage ChromeDriver binary.

    Returns:
        WebDriver: Local Chrome WebDriver instance

    Raises:
        Exception: If driver creation fails
    """
    logger.debug("Setting up local Chrome options")
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        logger.debug("Chrome options configured")

        driver_path = ChromeDriverManager().install()
        logger.debug(f"ChromeDriver path: {driver_path}")
        driver = webdriver.Chrome(service=ChromeService(driver_path), options=options)
        logger.info("Local Chrome WebDriver created successfully")
        driver.maximize_window()
        return driver
    except Exception as e:
        logger.error(f"Failed to create local WebDriver: {e}", exc_info=True)
        raise


def get_remote_driver(hub_url):
    """Create a Chrome WebDriver connected to Selenium Hub.

    Enables distributed testing across multiple machines/containers.

    Args:
        hub_url (str): Selenium Hub URL (e.g., http://selenium-hub:4444)

    Returns:
        WebDriver: Remote Chrome WebDriver instance

    Raises:
        Exception: If driver creation fails
    """
    logger.debug(f"Setting up remote Chrome options for {hub_url}")
    try:
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        logger.debug("Chrome options configured for remote")

        grid_url = f"{hub_url}/wd/hub" if not hub_url.endswith("/wd/hub") else hub_url
        logger.debug(f"Connecting to Selenium Grid at: {grid_url}")
        driver = webdriver.Remote(command_executor=grid_url, options=options)
        logger.info(f"Remote Chrome WebDriver created successfully via {grid_url}")
        driver.maximize_window()
        return driver
    except Exception as e:
        logger.error(f"Failed to create remote WebDriver: {e}", exc_info=True)
        raise
