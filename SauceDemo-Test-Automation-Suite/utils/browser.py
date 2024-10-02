from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_driver():
    """
    This function sets up and returns a headless Chrome WebDriver instance.

    Steps:
    1. Create ChromeOptions object to configure the browser.
    2. Set 'headless' mode to run the browser in the background.
    3. Add additional options (optional):
        - '--no-sandbox': disables sandbox for Chrome (might be needed for certain systems)
        - '--disable-dev-shm-usage': disables shared memory usage for Chrome (might be needed for certain systems)
    4. Use ChromeDriverManager to find the appropriate ChromeDriver and create a ChromeService instance.
    5. Create a new Chrome WebDriver instance using the ChromeService and options.
    6. Maximize the browser window (optional).
    7. Return the WebDriver instance.
    """

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Optional, might be needed for certain systems
    options.add_argument("--disable-dev-shm-usage")  # Optional, might be needed for certain systems
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.maximize_window()  # Optional
    return driver