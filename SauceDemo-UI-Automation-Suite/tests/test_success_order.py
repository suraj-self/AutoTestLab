from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.success_page import SuccessPage


def test_cart_success(browser):
    """
    Test case for successful login, adding an item to cart, checkout, and order placement.

    Steps:
    1. Navigate to the login page.
    2. Login with valid credentials ("standard_user", "secret_sauce").
    3. Assert successful login by checking the URL ("inventory.html").
    4. On the Inventory Page:
        - Search for a product ("Sauce Labs Onesie").
        - Add the product to the cart.
        - Assert the product is added successfully ("Remove" in the button text).
    5. On the Cart Page:
        - Proceed to checkout.
        - Verify added product details (assertion using a dictionary).
        - Click the checkout button.
        - Assert successful navigation to checkout page URL ("checkout-step-one.html").
    6. On the Checkout Page:
        - Enter checkout information: first name, last name, zip code.
        - Click continue and finish buttons.
        - Assert successful order placement by checking the URL ("checkout-complete.html").
    7. On the Success Page:
        - Verify success message ("Thank you for your order!").
    """

    # Navigate to login page
    browser.get("https://www.saucedemo.com/")

    # Login with valid credentials
    login_page_object = LoginPage(browser)
    login_page_object.enter_username("standard_user")
    login_page_object.enter_password("secret_sauce")
    login_page_object.click_login()

    # Validate successful login
    assert "inventory.html" in browser.current_url, "Login failed!"

    # Actions on Inventory Page with assertions
    inventory_page = InventoryPage(browser)
    inventory_page.search_product("Sauce Labs Onesie")
    text = inventory_page.add_to_cart()
    assert "Remove" in text, "Add to cart failed!"

    # Actions on Cart Page with assertions
    cart_page_object = CartPage(browser)
    cart_page_object.proceed_cart()
    message = cart_page_object.verify_added_product()
    assert message == {"message": "Item found", "messageCode": 200}
    cart_page_object.checkout_button()
    assert "checkout-step-one.html" in browser.current_url, "Checkout failed!"

    # Actions on Checkout Page with assertions
    checkout_page = CheckoutPage(browser)
    checkout_page.checkout_first_name("Max")
    checkout_page.checkout_last_name("Lee")
    checkout_page.checkout_zipcode("123456")
    checkout_page.click_continue()
    checkout_page.click_finish()
    assert "checkout-complete.html" in browser.current_url, "Order Placed failed!"

    # Actions on Success Page with assertion
    success_object = SuccessPage(browser)
    success_msg = success_object.verify_success_order()
    assert success_msg == "Thank you for your order!"
