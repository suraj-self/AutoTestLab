from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class InventoryPage:
    """
    This class represents the Inventory Page of the Sauce Demo application.

    Provides methods for interacting with elements on the inventory page,
    such as searching for products, adding products to the cart,
    and verifying successful addition.

    Attributes:
        driver (WebDriver): The WebDriver instance used to interact with the page.
        product_inventory (tuple): A tuple containing the locator for product name elements.
        add_to_cart_locator (tuple): A tuple containing the locator for the "Add To Cart" button.
        cart_flipped_text (tuple): A tuple containing the locator for the text that changes
                                    after adding an item to the cart (e.g., "REMOVE").
    """

    def __init__(self, driver):
        """
        Initializes the InventoryPage object with the provided WebDriver instance.

        Args:
            driver (WebDriver): The WebDriver instance used to interact with the page.
        """
        self.driver = driver
        self.product_inventory = (
            By.CLASS_NAME,
            "inventory_item_name",
        )  # Product name locator
        self.add_to_cart_locator = (
            By.ID,
            "add-to-cart",
        )  # "Add To Cart" button locator
        self.cart_flipped_text = (
            By.XPATH,
            "//*[@id='remove']",
        )  # Text indicating item in cart

    def search_product(self, product_name):
        """
        Searches for a product on the inventory page and clicks on it.

        Uses WebDriverWait with a 10-second timeout to wait for the product list to be present.
        Then iterates through each product name and clicks on the one that matches the provided name.

        Args:
            product_name (str): The name of the product to search for.
        """
        inventory_items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.product_inventory)
        )

        for product in inventory_items:
            if product_name in product.text:
                product.click()
                break

    def add_to_cart(self):
        """
        Clicks the "Add To Cart" button and returns the confirmation text.

        Uses WebDriverWait with a 10-second timeout to wait for the button to be clickable.
        Then clicks the button and uses WebDriverWait again to wait for a confirmation text to appear
        (e.g., the text might change from "Add To Cart" to "REMOVE").

        Returns:
            str: The confirmation text that appears after adding an item to the cart.
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_to_cart_locator)
        ).click()

        return (
            WebDriverWait(self.driver, 10)
            .until(EC.element_to_be_clickable(self.cart_flipped_text))
            .text
        )
