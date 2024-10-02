import pytest
from utils.browser import get_driver

@pytest.fixture
def browser():
    """
    Fixture to set up and tear down a WebDriver instance.

    Yields:
        webdriver: A WebDriver instance.

    Steps:
    1. Call the `get_driver()` function to obtain a WebDriver instance.
    2. Yield the WebDriver instance to the test.
    3. After the test finishes, call `driver.quit()` to close the browser.
    """

    driver = get_driver()
    yield driver
    driver.quit()