from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_inventory_success(browser):
    """
    Test case for successful login and adding a product to the cart.

    Steps:
    1. **Navigate to login page:** Open the Sauce Demo login page using the provided URL.
    2. **Perform login:**
        - Create a LoginPage object to interact with login page elements.
        - Enter the username ("standard_user").
        - Enter the password ("secret_sauce").
        - Click the login button to submit credentials.
    3. **Validate successful login:**
        - Verify that the current URL contains "inventory.html". This indicates successful navigation to the inventory page after login.
    4. **Interact with Inventory Page:**
        - Create an InventoryPage object to interact with elements on the inventory page.
        - Call the search_product method to find a specific product ("Sauce Labs Onesie").
        - Call the add_to_cart method to add the product to the cart.
        - Store the returned text from add_to_cart (might indicate success or failure).
    5. **Validate adding product to cart:**
        - Assert that the text returned by add_to_cart contains "Remove". This suggests the product was successfully added as the button text changes to "Remove".
    """
    # Navigate to login page
    browser.get("https://www.saucedemo.com/")

    # Login with valid credentials
    login_page = LoginPage(browser)
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()

    # Validate successful login
    assert "inventory.html" in browser.current_url, "Login failed!"

    # Search for product on Inventory Page
    inventory_page = InventoryPage(browser)
    inventory_page.search_product("Sauce Labs Onesie")
    text = inventory_page.add_to_cart()
    assert "Remove" in text, "Add to cart failed!"
