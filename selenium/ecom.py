from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup WebDriver
options = webdriver.ChromeOptions()
options.headless = False
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

try:
    # Navigate to the URL
    driver.get('https://www.saucedemo.com/')

    # Validate if the logo text includes 'Swag Labs'
    logo_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'login_logo'))
    ).text
    if 'Swag Labs' in logo_text:
        print('Text validation passed.')
    else:
        print('Text validation failed.')

    # Enter username and password
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'user-name'))
    )
    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )

    username_value = os.getenv('USERNAME')
    password_value = os.getenv('PASSWORD')
    
    if username_value is None or password_value is None:
        raise ValueError('Environment variables USERNAME and PASSWORD must be set.')

    username.send_keys(username_value)
    password.send_keys(password_value)

    # Click login button
    login_button = driver.find_element(By.ID, 'login-button')
    login_button.click()

    print('Logged in successfully.')

    # Validate if the title text includes 'Products'
    title_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'title'))
    ).text
    if 'Products' in title_text:
        print('Products text validation passed.')
    else:
        print('Products text validation failed.')

    # Click on 'Sauce Labs Onesie' product
    product_names = driver.find_elements(By.CLASS_NAME, 'inventory_item_name')
    if product_names is None:
        raise ValueError('No products found.')

    for product in product_names:
        if 'Sauce Labs Onesie' in product.text:
            product.click()
            break

    print('Clicked on "Sauce Labs Onesie".')

    # Validate if the product details name includes 'Sauce Labs Onesie'
    product_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'inventory_details_name'))
    ).text
    if 'Sauce Labs Onesie' in product_name:
        print('Product name validation passed.')
    else:
        print('Product name validation failed.')

    # Validate if the price text includes '$'
    price_text = driver.find_element(By.CLASS_NAME, 'inventory_details_price').text
    if '$' in price_text:
        print('Price validation passed.')
    else:
        print('Price validation failed.')

    # Click on 'Add to cart' button
    add_to_cart = driver.find_element(By.XPATH, '//*[@id="add-to-cart"]')
    add_to_cart.click()
    print('Clicked on "Add to cart" button.')

    # Click on the shopping cart link
    cart_link = driver.find_element(By.CLASS_NAME, 'shopping_cart_link')
    cart_link.click()
    print('Clicked on shopping cart icon.')

    # Validate if 'Sauce Labs Onesie' is found in the cart items
    cart_items = driver.find_elements(By.CLASS_NAME, 'cart_item')
    if cart_items is None:
        raise ValueError('No cart items found.')

    if any('Sauce Labs Onesie' in item.text for item in cart_items):
        print('Product "Sauce Labs Onesie" found in the cart.')
    else:
        print('Product "Sauce Labs Onesie" not found in the cart.')

    # Click on the 'Checkout' button
    checkout = driver.find_element(By.ID, 'checkout')
    checkout.click()
    print('Clicked on "Checkout" button.')

    # Validate if the checkout header text includes 'Checkout: Your Information'
    checkout_header_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'title'))
    ).text
    if 'Checkout: Your Information' in checkout_header_text:
        print('Checkout header text validation passed.')
    else:
        print('Checkout header text validation failed.')

    # Fill in checkout information
    driver.find_element(By.ID, 'first-name').send_keys('John')
    driver.find_element(By.ID, 'last-name').send_keys('Doe')
    driver.find_element(By.ID, 'postal-code').send_keys('12345')

    # Click on the 'Continue' button
    continue_button = driver.find_element(By.ID, 'continue')
    continue_button.click()
    print('Clicked on "Continue" button.')

    # Validate if the 'Finish' button text includes 'Finish'
    finish_button_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'finish'))
    ).text
    if 'Finish' in finish_button_text:
        print('Finish button text validation passed.')
    else:
        print('Finish button text validation failed.')

    # Click on the 'Finish' button
    finish_button = driver.find_element(By.ID, 'finish')
    finish_button.click()
    print('Clicked on "Finish" button.')

    # Validate if the 'Thank you' text includes 'Thank you for your order!'
    thank_you_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'complete-header'))
    ).text
    if 'Thank you for your order!' in thank_you_text:
        print('Thank you text validation passed.')
    else:
        print('Thank you text validation failed.')

    # Click on the 'Back Home' button
    back_home = driver.find_element(By.ID, 'back-to-products')
    back_home.click()
    print('Clicked on "Back Home" button.')

    # Validate if the title text includes 'Products'
    products_header_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'title'))
    ).text
    if 'Products' in products_header_text:
        print('Products text validation passed.')
    else:
        print('Products text validation failed.')

    # Additional steps for logging out
    burger_menu_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'bm-burger-button'))
    )
    burger_menu_button.click()
    print('Clicked on lines icon')


    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'logout_sidebar_link'))
    )
    logout_link.click()
    print('Clicked on the Logout link.')

    # Validate if the login button text is 'Login'
    login_button_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'login-button'))
    ).get_attribute('value')
    if login_button_text == 'Login':
        print('The login button text is correct.')
    else:
        print('The login button text is incorrect. Found:', login_button_text)

    print('Script execution completed.')

except Exception as e:
    print(f'Error occurred: {e}')

finally:
    driver.quit()
