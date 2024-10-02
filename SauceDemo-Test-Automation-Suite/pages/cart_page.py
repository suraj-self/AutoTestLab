from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    def __init__(self, driver):
        """
        Initializes the CartPage object with the provided WebDriver instance.

        Args:
            driver (WebDriver): The WebDriver instance used to interact with the page.
        """
        self.driver = driver
        self.cart_link_locator = (By.XPATH, "//*[@id='shopping_cart_container']/a")  # Locator for shopping cart link
        self.added_product_locator = (By.CLASS_NAME, "inventory_item_name")  # Locator for added product name
        self.checkout_locator = (By.ID, "checkout")  # Locator for "Checkout" button
        self.checkout_title = (By.CLASS_NAME, 'title')  # Locator for checkout page title (unused in current methods)

    def proceed_cart(self):
        """
        Clicks the shopping cart link to open the cart page.

        Uses WebDriverWait with a 10-second timeout to wait for the cart link to be clickable
        before clicking it.
        """
        cart_link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.cart_link_locator))
        cart_link.click()

    def verify_added_product(self):
        """
        Verifies if the expected product ("Sauce Labs Onesie") is present in the cart.

        Uses WebDriverWait with a 10-second timeout to wait for the product name element to be clickable.
        Then gets the product name text and compares it to the expected product name.
        Returns a dictionary with a message and message code based on the result:

        - {"message": "Item found", "messageCode": 200} : If the expected product is found.
        - {"message": "Item not found", "messageCode": 400} : If the expected product is not found.

        Raises:
            TimeoutException: If the product name element is not found within the timeout.
        """
        cart_items = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.added_product_locator)).text

        if cart_items == "Sauce Labs Onesie":
            return {"message": "Item found", "messageCode": 200}
        else:
            return {"message": "Item not found", "messageCode": 400}

    def checkout_button(self):
        """
        Clicks the "Checkout" button on the cart page to proceed to checkout.

        Uses WebDriverWait with a 10-second timeout to wait for the button to be clickable before clicking.
        """
        checkout_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.checkout_locator))
        checkout_button.click()