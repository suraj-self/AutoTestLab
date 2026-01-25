from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_cart_success(browser):
    # Navigate to login page
    browser.get("https://www.saucedemo.com/")

    # Login with valid credentials
    login_page_object = LoginPage(browser)
    login_page_object.enter_username("standard_user")
    login_page_object.enter_password("secret_sauce")
    login_page_object.click_login()

    # Validate successful login
    assert "inventory.html" in browser.current_url, "Login failed!"

    # Search for product on Inventory Page
    inventory_page = InventoryPage(browser)
    inventory_page.search_product("Sauce Labs Onesie")

    # Add product to cart
    text = inventory_page.add_to_cart()
    assert "Remove" in text, "Add to cart failed!"

    # Proceed to checkout from Cart Page
    cart_page_object = CartPage(browser)
    cart_page_object.proceed_cart()

    # Verify added product details
    message = cart_page_object.verify_added_product()
    assert message == {"message": "Item found", "messageCode": 200}

    # Click checkout button
    cart_page_object.checkout_button()

    # Validate checkout page URL
    assert "checkout-step-one.html" in browser.current_url, "Checkout failed!"
