from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SuccessPage:
    """
    This class represents the Success Page of the Sauce Demo application.

    Attributes:
        driver (WebDriver): The WebDriver instance used to interact with the page.
        success_message (tuple): A tuple containing the locator for the success message element.
        back_home (tuple): A tuple containing the locator for the "Back To Products" button.
    """

    def __init__(self, driver):
        """
        Initializes the SuccessPage object with the provided WebDriver instance.

        Args:
            driver (WebDriver): The WebDriver instance used to interact with the page.
        """
        self.driver = driver
        self.success_message = (By.XPATH, "//*[@id='checkout_complete_container']/h2")
        self.back_home = (By.ID, "back-to-products")

    def verify_success_order(self):
        """
        Verifies the presence of the success message element and returns its text.

        Uses WebDriverWait with a 10-second timeout to wait for the element to be present.
        If the element is not found within the timeout, a TimeoutException is raised.

        Returns:
            str: The text of the success message element.
        """
        success_text = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.success_message)).text
        return success_text

    def click_back_home(self):
        """
        Clicks the "Back To Products" button on the Success Page.

        Uses WebDriverWait with a 10-second timeout to wait for the button to be clickable.
        If the button is not clickable within the timeout, a TimeoutException is raised.
        """
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.back_home)).click()