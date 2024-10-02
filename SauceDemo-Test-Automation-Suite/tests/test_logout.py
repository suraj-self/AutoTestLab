from pages.login_page import LoginPage
from pages.logout_page import LogoutPage

def test_logout_success(browser):
    """
    Test case for successful login and logout on Sauce Demo.

    Steps:
    1. **Navigate to login page:** Open the Sauce Demo login page.
    2. **Perform login:**
        - Create a LoginPage object to interact with login page elements.
        - Enter valid username ("standard_user").
        - Enter valid password ("secret_sauce").
        - Click the login button to submit credentials.
    3. **Validate successful login:**
        - Assert that the current URL contains "inventory.html", indicating successful navigation to the inventory page.
    4. **Perform logout:**
        - Create a LogoutPage object to interact with logout page elements.
        - Click the menu icon (if applicable).
        - Click the "Logout" button to log out of the application.
    5. **Validate successful logout:**
        - Assert that the current URL contains "www.saucedemo.com", indicating successful logout and navigation back to the login page.
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

    # Logout after login
    logout_object = LogoutPage(browser)
    logout_object.click_menu_icon()  # Click menu icon if necessary
    logout_object.click_logout()
    assert "www.saucedemo.com" in browser.current_url, "Logout failed!"