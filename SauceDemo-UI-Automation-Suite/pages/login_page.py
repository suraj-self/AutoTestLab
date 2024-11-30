from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """
    This class represents the Login Page of the Sauce Demo application.

    Provides methods for interacting with login page elements,
    such as entering username and password, and submitting the login form.

    Attributes:
        driver (WebDriver): The WebDriver instance used to interact with the page.
        username (tuple): A tuple containing the locator for the username input field.
        password (tuple): A tuple containing the locator for the password input field.
        submit (tuple): A tuple containing the locator for the login button.
    """

    def __init__(self, driver):
        """
        Initializes the LoginPage object with the provided WebDriver instance.

        Args:
            driver (WebDriver): The WebDriver instance used to interact with the page.
        """
        self.driver = driver
        self.username = (By.ID, "user-name")  # Username locator
        self.password = (By.ID, "password")  # Password locator
        self.submit = (By.ID, "login-button")  # Submit locator (login button)

    def enter_username(self, username):
        """
        Enters the provided username into the username input field.

        Uses WebDriverWait with a 10-second timeout to wait for the element
        to be present before sending the keys.

        Args:
            username (str): The username to enter.
        """
        username_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.username))
        username_field.send_keys(username)

    def enter_password(self, password):
        """
        Enters the provided password into the password input field.

        Uses WebDriverWait with a 10-second timeout to wait for the element
        to be present before sending the keys.

        Args:
            password (str): The password to enter.
        """
        password_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.password))
        password_field.send_keys(password)

    def click_login(self):
        """
        Clicks the login button to submit the login form.

        Uses WebDriverWait with a 10-second timeout to wait for the element
        to be clickable before clicking.

        Raises a TimeoutException if the button is not clickable within the timeout.
        """
        login_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.submit))
        login_button.click()