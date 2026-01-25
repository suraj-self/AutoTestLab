from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class CheckoutPage:
    """
    This class represents the Checkout Page of the Sauce Demo application.

    Provides methods for interacting with elements on the checkout page,
    such as entering shipping information and submitting the order.

    Attributes:
        driver (WebDriver): The WebDriver instance used to interact with the page.
        first_name_locator (tuple): A tuple containing the locator for the first name input field.
        last_name_locator (tuple): A tuple containing the locator for the last name input field.
        zip_code_locator (tuple): A tuple containing the locator for the zip code input field.
        continue_locator (tuple): A tuple containing the locator for the "Continue" button.
        finish_locator (tuple): A tuple containing the locator for the "Finish" button.
    """

    def __init__(self, driver):
        """
        Initializes the CheckoutPage object with the provided WebDriver instance.

        Args:
            driver (WebDriver): The WebDriver instance used to interact with the page.
        """
        self.driver = driver
        self.first_name_locator = (By.ID, "first-name")
        self.last_name_locator = (By.ID, "last-name")
        self.zip_code_locator = (By.ID, "postal-code")
        self.continue_locator = (By.ID, "continue")
        self.finish_locator = (By.ID, "finish")

    def checkout_first_name(self, first_name):
        """
        Enters the provided first name into the first name input field on the checkout page.

        Uses WebDriverWait with a 10-second timeout to wait for the element to be clickable
        before sending the keys.

        Args:
            first_name (str): The first name to enter.
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.first_name_locator)
        ).send_keys(first_name)

    def checkout_last_name(self, last_name):
        """
        Enters the provided last name into the last name input field on the checkout page.

        Uses WebDriverWait with a 10-second timeout to wait for the element to be clickable
        before sending the keys.

        Args:
            last_name (str): The last name to enter.
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.last_name_locator)
        ).send_keys(last_name)

    def checkout_zipcode(self, zip_code):
        """
        Enters the provided zip code into the zip code input field on the checkout page.

        Uses WebDriverWait with a 10-second timeout to wait for the element to be clickable
        before sending the keys.

        Args:
            zip_code (str): The zip code to enter.
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.zip_code_locator)
        ).send_keys(zip_code)

    def click_continue(self):
        """
        Clicks the "Continue" button on the checkout page.

        Uses WebDriverWait with a 10-second timeout to wait for the button to be clickable before clicking.
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.continue_locator)
        ).click()

    def click_finish(self):
        """
        Clicks the "Finish" button on the checkout page.

        Uses WebDriverWait with a 10-second timeout to wait for the button to be clickable before clicking.
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.finish_locator)
        ).click()
