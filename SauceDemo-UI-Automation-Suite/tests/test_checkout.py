from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_cart_success(browser):
    """
    This test verifies the functionality of adding an item to the cart,
    proceeding to checkout, and successfully placing an order.

    Steps:
        1. Navigate to the login page of the Sauce Demo application.
        2. Login with a standard user.
        3. Verify successful login by checking the URL.
        4. Search for a specific product ("Sauce Labs Onesie").
        5. Add the product to the cart and verify the action.
        6. Open the cart page.
        7. Verify the added product in the cart.
        8. Proceed to checkout and verify the URL.
        9. Fill in the checkout form with dummy data.
        10. Click "Continue" and "Finish" buttons.
        11. Verify order placed successfully by checking the URL.
    """

    # 1. Navigate to the login page
    browser.get("https://www.saucedemo.com/")

    # 2. Login with a standard user
    login_page_object = LoginPage(browser)
    login_page_object.enter_username("standard_user")
    login_page_object.enter_password("secret_sauce")
    login_page_object.click_login()

    # 3. Verify successful login
    assert "inventory.html" in browser.current_url, "Login failed!"

    # 4. Search for a specific product
    inventory_page = InventoryPage(browser)
    inventory_page.search_product("Sauce Labs Onesie")

    # 5. Add the product to the cart and verify the action
    text = inventory_page.add_to_cart()
    assert "Remove" in text, "Add to cart failed!"

    # 6. Open the cart page
    cart_page_object = CartPage(browser)
    cart_page_object.proceed_cart()

    # 7. Verify the added product in the cart
    message = cart_page_object.verify_added_product()
    assert message == {"message": "Item found", "messageCode": 200}

    # 8. Proceed to checkout and verify the URL
    cart_page_object.checkout_button()
    assert "checkout-step-one.html" in browser.current_url, "Checkout failed!"

    # 9. Fill in the checkout form with dummy data
    checkout_page = CheckoutPage(browser)
    checkout_page.checkout_first_name("Max")
    checkout_page.checkout_last_name("Lee")
    checkout_page.checkout_zipcode("123456")

    # 10. Click "Continue" and "Finish" buttons
    checkout_page.click_continue()
    checkout_page.click_finish()

    # 11. Verify order placed successfully
    assert "checkout-complete.html" in browser.current_url, "Order Placed failed!"
