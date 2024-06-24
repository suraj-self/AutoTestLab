const puppeteer = require('puppeteer');
require('dotenv').config(); // Load environment variables from a .env file

puppeteer.launch({ headless: false, slowMo: 50 }) // Launch Puppeteer in non-headless mode with a slight slowdown for visibility
  .then(browser => browser.newPage() // Create a new page in the opened browser instance
    .then(page => {
      return page.goto('https://www.saucedemo.com/') // Navigate to the URL
        .then(() => page.$eval('.login_logo', el => el.textContent)) // Extract text content of the .login_logo element
        .then(logoText => {
          // Validate if the logo text includes 'Swag Labs'
          if (logoText.includes('Swag Labs')) {
            console.log('Text validation passed.');
          } else {
            console.log('Text validation failed.');
          }
          // Wait for the username input field to appear
          return page.waitForSelector('#user-name');
        })
        .then(() => page.type('#user-name', process.env.USERNAME)) // Type the username fetched from environment variables
        .then(() => page.waitForSelector('#password')) // Wait for the password input field to appear
        .then(() => page.type('#password', process.env.PASSWORD)) // Type the password fetched from environment variables
        .then(() => page.waitForSelector('#login-button')) // Wait for the login button to appear
        .then(() => page.click('#login-button')) // Click on the login button
        .then(() => {
          console.log('Logged in successfully.');
          // Wait for the title element to appear on the inventory page
          return page.waitForSelector('.title');
        })
        .then(() => page.$eval('.title', el => el.textContent)) // Extract text content of the title element
        .then(titleText => {
          // Validate if the title text includes 'Products'
          if (titleText.includes('Products')) {
            console.log('Products text validation passed.');
          } else {
            console.log('Products text validation failed.');
          }
          // Wait for the product name elements to appear
          return page.waitForSelector('.inventory_item_name');
        })
        .then(() => page.$$eval('.inventory_item_name', elements => elements.map(el => el.textContent))) // Extract text content of all product name elements
        .then(productNames => {
          const productIndex = productNames.indexOf('Sauce Labs Onesie');
          if (productIndex !== -1) {
            // Calculate the selector for the product based on its index
            const productSelector = `.inventory_item:nth-child(${productIndex + 1}) .inventory_item_name`;
            // Click on the product based on the generated selector
            return page.click(productSelector)
              .then(() => {
                console.log('Clicked on "Sauce Labs Onesie".');
                // Wait for the product details name element to appear
                return page.waitForSelector('.inventory_details_name');
              })
              .then(() => page.$eval('.inventory_details_name', el => el.textContent)) // Extract text content of the product details name element
              .then(productName => {
                // Validate if the product details name includes 'Sauce Labs Onesie'
                if (productName.includes('Sauce Labs Onesie')) {
                  console.log('Product name validation passed.');
                } else {
                  console.log('Product name validation failed.');
                }
                // Extract text content of the product details price element
                return page.$eval('.inventory_details_price', el => el.textContent);
              })
              .then(priceText => {
                // Validate if the price text includes '$'
                if (priceText.includes('$')) {
                  console.log('Price validation passed.');
                } else {
                  console.log('Price validation failed.');
                }
                // Wait for the 'Add to cart' button to appear
                return page.waitForSelector('#add-to-cart');
              })
              .then(() => page.click('#add-to-cart')) // Click on the 'Add to cart' button
              .then(() => {
                console.log('Clicked on "Add to cart" button.');
                // Wait for the shopping cart link to appear
                return page.waitForSelector('a.shopping_cart_link');
              })
              .then(() => page.click('a.shopping_cart_link')) // Click on the shopping cart link
              .then(() => {
                console.log('Clicked on shopping cart icon.');
                // Wait for the cart item elements to appear
                return page.waitForSelector('.cart_item');
              })
              .then(() => page.$$eval('.cart_item', elements => elements.map(el => el.textContent))) // Extract text content of all cart item elements
              .then(cartItems => {
                // Validate if 'Sauce Labs Onesie' is found in the cart items
                if (cartItems.some(item => item.includes('Sauce Labs Onesie'))) {
                  console.log('Product "Sauce Labs Onesie" found in the cart.');
                } else {
                  console.log('Product "Sauce Labs Onesie" not found in the cart.');
                }
                // Wait for the 'Checkout' button to appear
                return page.waitForSelector('#checkout');
              })
              .then(() => page.click('#checkout')) // Click on the 'Checkout' button
              .then(() => {
                console.log('Clicked on "Checkout" button.');
                // Wait for the title element to appear again
                return page.waitForSelector('.title');
              })
              .then(() => page.$eval('.title', el => el.textContent)) // Extract text content of the title element again
              .then(checkoutHeaderText => {
                // Validate if the checkout header text includes 'Checkout: Your Information'
                if (checkoutHeaderText.includes('Checkout: Your Information')) {
                  console.log('Checkout header text validation passed.');
                } else {
                  console.log('Checkout header text validation failed.');
                }
                // Wait for the 'First Name' input field to appear
                return page.waitForSelector('#first-name');
              })
              .then(() => page.type('#first-name', 'John')) // Type 'John' into the 'First Name' input field
              .then(() => page.waitForSelector('#last-name')) // Wait for the 'Last Name' input field to appear
              .then(() => page.type('#last-name', 'Doe')) // Type 'Doe' into the 'Last Name' input field
              .then(() => page.waitForSelector('#postal-code')) // Wait for the 'Postal Code' input field to appear
              .then(() => page.type('#postal-code', '12345')) // Type '12345' into the 'Postal Code' input field
              .then(() => page.waitForSelector('#continue')) // Wait for the 'Continue' button to appear
              .then(() => page.click('#continue')) // Click on the 'Continue' button
              .then(() => {
                console.log('Clicked on "Continue" button.');
                // Wait for the 'Finish' button to appear
                return page.waitForSelector('#finish');
              })
              .then(() => page.$eval('#finish', el => el.textContent)) // Extract text content of the 'Finish' button
              .then(finishButtonText => {
                // Validate if the 'Finish' button text includes 'Finish'
                if (finishButtonText.includes('Finish')) {
                  console.log('Finish button text validation passed.');
                } else {
                  console.log('Finish button text validation failed.');
                }
                // Wait for the 'Finish' button to appear again
                return page.waitForSelector('#finish');
              })
              .then(() => page.click('#finish')) // Click on the 'Finish' button
              .then(() => {
                console.log('Clicked on "Finish" button.');
                // Wait for the 'Complete' header to appear
                return page.waitForSelector('.complete-header');
              })
              .then(() => page.$eval('.complete-header', el => el.textContent)) // Extract text content of the 'Complete' header
              .then(thankYouText => {
                // Validate if the 'Thank you' text includes 'Thank you for your order!'
                if (thankYouText.includes('Thank you for your order!')) {
                  console.log('Thank you text validation passed.');
                } else {
                  console.log('Thank you text validation failed.');
                }
                // Wait for the 'Back to Products' button to appear
                return page.waitForSelector('#back-to-products');
              })
              .then(() => page.click('#back-to-products')) // Click on the 'Back to Products' button
              .then(() => {
                console.log('Clicked on "Back Home" button.');
                // Wait for the title element to appear again
                return page.waitForSelector('.title');
              })
              .then(() => page.$eval('.title', el => el.textContent)) // Extract text content of the title element again
              .then(productsHeaderText => {
                // Validate if the title text includes 'Products'
                if (productsHeaderText.includes('Products')) {
                  console.log('Products text validation passed.');
                } else {
                  console.log('Products text validation failed.');
                }

                // Additional steps for logging out
                // Wait for the burger menu button to appear
                return page.waitForSelector('.bm-burger-button', { visible: true });
              })
              .then(() => page.click('.bm-burger-button')) // Click on the burger menu button
              .then(() => {
                console.log('Clicked on lines icon');
                // Wait for the logout link to appear
                return page.waitForSelector('a#logout_sidebar_link.bm-item.menu-item', { visible: true });
              })
              .then(() => page.evaluate(() => {
                // Scroll the logout link into view
                const logoutLink = document.querySelector('a#logout_sidebar_link.bm-item.menu-item');
                logoutLink.scrollIntoView();
              }))
              .then(() => page.$eval('a#logout_sidebar_link.bm-item.menu-item', (elem) => {
                // Evaluate if the logout link is clickable
                const rect = elem.getBoundingClientRect();
                return (
                  rect.width > 0 &&
                  rect.height > 0 &&
                  window.getComputedStyle(elem).visibility !== 'hidden' &&
                  window.getComputedStyle(elem).display !== 'none'
                );
              }))
              .then(isClickable => {
                if (isClickable) {
                  // Click on the logout link if it's clickable
                  return page.click('a#logout_sidebar_link.bm-item.menu-item').then(() => {
                    console.log('Clicked on the Logout link.');
                    // Wait for the login button to appear again
                    return page.waitForSelector('#login-button');
                  });
                } else {
                  throw new Error('Logout link is not clickable');
                }
              })
              .then(() => page.$eval('#login-button', el => el.value)) // Extract the text content of the login button
              .then(loginButtonValue => {
                // Validate if the login button text is 'Login'
                if (loginButtonValue === 'Login') {
                  console.log('The login button text is correct.');
                } else {
                  console.log('The login button text is incorrect. Found:', loginButtonValue);
                }
                console.log('Script execution completed.');
                // Close the browser instance
                return browser.close();
              })
              .catch(err => {
                // Handle and log errors during script execution
                console.error('Error occurred:', err);
                // Close the browser instance in case of error
                return browser.close();
              });
          } else {
            console.log('"Sauce Labs Onesie" not found.');
            // Close the browser instance if 'Sauce Labs Onesie' is not found
            return browser.close();
          }
        });
    }))
  .catch(err => {
    // Handle and log errors during Puppeteer launch or page creation
    console.error('Error occurred:', err);
  });
