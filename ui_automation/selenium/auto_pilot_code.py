import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

def run_selenium_script():
    # Setup logging
    logging.basicConfig(filename='test_execution.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    # Load environment variables
    load_dotenv()

    # Read sensitive data from .env
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')

    driver = None  # Initialize the driver variable
    try:
        # Read non-sensitive data from testData.json
        with open('data/testData.json') as json_file:
            test_data = json.load(json_file)

        # Setup chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Use headless mode for CI/CD
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        logging.info("Browser launched successfully")

        # Navigate to login page
        driver.get(test_data["url"])
        logging.info("Navigated to login page")

        # Wait for the "Swag Labs" logo to be visible
        login_logo = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'login_logo'))
        )
        logo_text = login_logo.text
        if logo_text != 'Swag Labs':
            logging.error("Swag Labs text not found on login page")
            return {"message": "fail", "messageCode": 400}

        # Wait for username field and enter login credentials
        usrname_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'user-name'))
        )
        usrname_field.send_keys(USERNAME)
        logging.info("Entered username")

        usrpwd_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'password'))
        )
        usrpwd_field.send_keys(PASSWORD)
        logging.info("Entered password")

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'login-button'))
        )
        login_button.click()

        # Wait for home page title to appear
        home_page_title_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'title'))
        )
        home_page_title_text = home_page_title_element.text
        if home_page_title_text != 'Products':
            logging.error("Home page title is incorrect")
            return {"message": "fail", "messageCode": 400}

        # Find specific product
        inventory_items_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'inventory_item_name'))
        )
        if not inventory_items_list:
            logging.error("No product found")
            return {"message": "fail", "messageCode": 400}

        for product in inventory_items_list:
            if test_data["product_name"] in product.text:
                logging.info(f"Found product: {test_data['product_name']}")
                product.click()
                break

        # Wait for the price element and validate product price contains '$'
        price_elem = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'inventory_details_price'))
        )
        price_text = price_elem.text
        if '$' not in price_text:
            logging.error("Price does not contain $")
            return {"message": "fail", "messageCode": 400}

        # Add to cart
        add_cart_elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'add-to-cart'))
        )
        add_cart_elem.click()
        logging.info("Added item to cart")
        
        # Wait for and click on cart icon
        cart_icon_elements = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'shopping_cart_link'))
        )
        cart_icon_elements.click()
        logging.info("Clicked on cart icon")

        # Validate item in cart
        cart_item_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'cart_item'))
        )
        if any(test_data["product_name"] in item.text for item in cart_item_elem):
            logging.info(f"Product {test_data['product_name']} found in the cart.")
        else:
            logging.error("Product not found in cart")
            return {"message": "fail", "messageCode": 400}

        # Proceed to checkout
        checkout_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'checkout'))
        )
        checkout_element.click()
        logging.info("Proceeded to checkout")

        # Fill in checkout details
        first_name_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'first-name'))
        )
        first_name_elem.send_keys(test_data['first_name'])
        logging.info("Entered first name")

        last_name_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'last-name'))
        )
        last_name_elem.send_keys(test_data['last_name'])
        logging.info("Entered last name")

        zip_code_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'postal-code'))
        )
        zip_code_elem.send_keys(test_data['zip_code'])
        logging.info("Entered zip code")

        # Continue checkout process
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'continue'))
        )
        continue_button.click()
        logging.info("Clicked on 'Continue' button")

        finish_button_elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'finish'))
        )
        finish_button_elem.click()
        logging.info("Clicked on 'Finish' button")

        # Validate order confirmation
        order_confirm_msg_elem = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'complete-header'))
        )
        order_confirm_msg_text = order_confirm_msg_elem.text
        if order_confirm_msg_text != "Thank you for your order!":
            logging.error("Order confirmation message is incorrect")
            return {"message": "fail", "messageCode": 400}
        else:
            logging.info("Order placed successfully")

        # Log out
        burger_menu_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'bm-burger-button'))
        )
        burger_menu_button.click()
        logging.info("Clicked on burger menu")

        logout_link_elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'logout_sidebar_link'))
        )
        logout_link_elem.click()
        logging.info("Logged out successfully")

        return {"message": "success", "messageCode": 200}
    
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return {"message": "fail", "messageCode": 400}
    
    finally:
        if driver:
            driver.quit()  # Quit the browser if the driver is initialized
            logging.info("Browser closed")

# Add this to call the function when the script is executed
if __name__ == "__main__":
    result = run_selenium_script()
    print(result)  # This will print the success/failure message and messageCode
