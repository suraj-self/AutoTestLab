from pages.login_page import LoginPage


def test_login_success(browser):
    """
    Test case for successful login on Sauce Demo website.

    Steps:
    1. Navigate to the login page URL.
    2. Initialize a LoginPage object with the browser instance.
    3. Use the LoginPage object methods to perform login actions:
        - enter_username("standard_user")
        - enter_password("secret_sauce")
        - click_login()
    4. Assertion: Verify if the current URL contains "inventory.html", indicating successful login.
    """

    # navigate to login page
    browser.get("https://www.saucedemo.com/")

    # initialize LoginPage object
    login_page = LoginPage(browser)

    # perform login action
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()

    # Add an assertion here (For example, check if login was successful)
    assert "inventory.html" in browser.current_url, "Login failed!"
