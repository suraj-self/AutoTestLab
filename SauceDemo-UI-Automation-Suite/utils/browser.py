import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    """
    This function sets up and returns a Chrome WebDriver instance.

    It supports two modes:
    1. Local execution: Uses local ChromeDriver with ChromeDriverManager
    2. Selenium Grid execution: Connects to remote Selenium Hub via environment variable

    Environment Variables:
    - SELENIUM_HUB_URL: URL to Selenium Hub (e.g., http://selenium-hub:4444)
    - USE_GRID: Set to 'true' to enable Selenium Grid mode (default: false)

    Returns:
        WebDriver: A Chrome WebDriver instance
    """

    use_grid = os.getenv("USE_GRID", "false").lower() == "true"
    selenium_hub_url = os.getenv("SELENIUM_HUB_URL", "http://localhost:4444")

    if use_grid:
        return get_remote_driver(selenium_hub_url)
    else:
        return get_local_driver()


def get_local_driver():
    """
    Sets up and returns a headless Chrome WebDriver instance for local execution.

    Uses ChromeDriverManager to automatically manage the ChromeDriver binary.

    Steps:
    1. Create ChromeOptions object to configure the browser.
    2. Set 'headless' mode to run the browser in the background.
    3. Add additional options for sandbox and shared memory handling.
    4. Use ChromeDriverManager to find the appropriate ChromeDriver.
    5. Create a new Chrome WebDriver instance.
    6. Maximize the browser window.

    Returns:
        WebDriver: A local Chrome WebDriver instance
    """

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )
    driver.maximize_window()
    return driver


def get_remote_driver(hub_url):
    """
    Sets up and returns a Chrome WebDriver instance connected to a Selenium Hub.

    This enables distributed testing across multiple machines/containers.

    Args:
        hub_url (str): URL to the Selenium Hub (e.g., http://selenium-hub:4444)

    Returns:
        WebDriver: A remote Chrome WebDriver instance
    """

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Selenium 4 uses /wd/hub for the endpoint
    grid_url = f"{hub_url}/wd/hub" if not hub_url.endswith("/wd/hub") else hub_url

    driver = webdriver.Remote(command_executor=grid_url, options=options)
    driver.maximize_window()
    return driver
