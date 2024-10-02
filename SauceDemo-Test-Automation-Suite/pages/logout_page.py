from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LogoutPage:
    """
    This class represents the Logout Page of the Sauce Demo application.

    Provides methods for interacting with elements on the logout page,
    such as clicking the menu icon (if present) and the logout button.

    Attributes:
        driver (WebDriver): The WebDriver instance used to interact with the page.
        menu_icon_locator (tuple): A tuple containing the locator for the menu icon element.
        logout_locator (tuple): A tuple containing the locator for the logout button element.
    """

    def __init__(self, driver):
        """
        Initializes the LogoutPage object with the provided WebDriver instance.

        Args:
            driver (WebDriver): The WebDriver instance used to interact with the page.
        """
        self.driver = driver
        self.menu_icon_locator = (By.ID, "react-burger-menu-btn")
        self.logout_locator = (By.ID, "logout_sidebar_link")

    def click_menu_icon(self):
        """
        Clicks the menu icon on the Logout Page (if present).

        Uses WebDriverWait with a 10-second timeout to wait for the element to be clickable.
        If the element is not found within the timeout, a TimeoutException is raised.

        This method is useful when the logout functionality requires clicking a menu first
        to access the logout option.
        """
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.menu_icon_locator)).click()

    def click_logout(self):
        """
        Clicks the logout button on the Logout Page.

        Uses WebDriverWait with a 10-second timeout to wait for the element to be clickable.
        If the element is not found within the timeout, a TimeoutException is raised.
        """
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.logout_locator)).click()