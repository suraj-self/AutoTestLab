// This Puppeteer script demonstrates automated testing
// for the web application https://www.saucedemo.com, a demo e-commerce site designed for testing purposes.
// Use Cases: Testing login functionality, product search, adding products to the cart, and the checkout process.
const puppeteer = require('puppeteer');
require('dotenv').config();
puppeteer.launch({ headless: false })
  .then(browser => browser.newPage()
    .then(page => {
      // Navigate to the page
      return page.goto('https://www.saucedemo.com/')
        .then(() => page.$eval('.login_logo', el => el.textContent))
        .then(logoText => {
          // Validate the text
          if (logoText.includes('Swag Labs')) {
            console.log('Text validation passed.');
          } else {
            console.log('Text validation failed.');
          }

          // Fill in the login form
          return page.waitForSelector('#user-name')
            .then(() => page.type('#user-name', process.env.USERNAME)) // Replace 'standard_user' with the actual username
            .then(() => page.waitForSelector('#password'))
            .then(() => page.type('#password', process.env.PASSWORD))
            .then(() => page.waitForSelector('#login-button'))
            .then(() => page.click('#login-button'))
            .then(() => {
              console.log('Logged in successfully.');
            })
            .then(() => page.waitForSelector('.title'))
            .then(() => page.$eval('.title', el => el.textContent))
            .then(titleText => {
              // Validate the "Products" text on the inventory page
              if (titleText.includes('Products')) {
                console.log('Products text validation passed.');
              } else {
                console.log('Products text validation failed.');
              }

              // Get all product names
              return page.waitForSelector('.inventory_item_name')
                .then(() => page.$$eval('.inventory_item_name', elements => elements.map(el => el.textContent)))
                .then(productNames => {
                  // Find index of 'Sauce Labs Onesie' and click on it
                  const productIndex = productNames.indexOf('Sauce Labs Onesie');
                  if (productIndex !== -1) {
                    const productSelector = `.inventory_item:nth-child(${productIndex + 1}) .inventory_item_name`;
                    return page.click(productSelector)
                      .then(() => {
                        console.log('Clicked on "Sauce Labs Onesie".');
                      })
                      .then(() => page.waitForSelector('.inventory_details_name'))
                      .then(() => page.$eval('.inventory_details_name', el => el.textContent))
                      .then(productName => {
                        // Validate product name
                        if (productName.includes('Sauce Labs Onesie')) {
                          console.log('Product name validation passed.');
                        } else {
                          console.log('Product name validation failed.');
                        }
                      })
                      .then(() => page.$eval('.inventory_details_price', el => el.textContent))
                      .then(priceText => {
                        // Validate price
                        if (priceText.includes('$')) {
                          console.log('Price validation passed.');
                        } else {
                          console.log('Price validation failed.');
                        }
                      })
                      .then(() => page.waitForSelector('#add-to-cart'))
                      .then(() => page.click('#add-to-cart'))
                      .then(() => {
                        console.log('Clicked on "Add to cart" button.');
                      })
                      .then(() => page.waitForSelector('a.shopping_cart_link'))
                      .then(() => page.click('a.shopping_cart_link'))
                      .then(() => {
                        console.log('Clicked on shopping cart icon.');
                      })
                      .then(() => page.waitForSelector('.cart_item'))
                      .then(() => page.$$eval('.cart_item', elements => elements.map(el => el.textContent)))
                      .then(cartItems => {
                        // Validate the product in the cart
                        if (cartItems.some(item => item.includes('Sauce Labs Onesie'))) {
                          console.log('Product "Sauce Labs Onesie" found in the cart.');
                        } else {
                          console.log('Product "Sauce Labs Onesie" not found in the cart.');
                        }
                      })
                      .then(() => page.waitForSelector('#checkout'))
                      .then(() => page.click('#checkout'))
                      .then(() => {
                        console.log('Clicked on "Checkout" button.');
                      })
                      .then(() => page.waitForSelector('.title'))
                      .then(() => page.$eval('.title', el => el.textContent))
                      .then(checkoutHeaderText => {
                        // Wait for the "Checkout: Your Information" text
                        if (checkoutHeaderText.includes('Checkout: Your Information')) {
                          console.log('Checkout header text validation passed.');
                        } else {
                          console.log('Checkout header text validation failed.');
                        }
                      })
                      .then(() => page.waitForSelector('#first-name'))
                      .then(() => page.type('#first-name', 'John')) // Replace with actual first name
                      .then(() => page.waitForSelector('#last-name'))
                      .then(() => page.type('#last-name', 'Doe')) // Replace with actual last name
                      .then(() => page.waitForSelector('#postal-code'))
                      .then(() => page.type('#postal-code', '12345')) // Replace with actual postal code
                      .then(() => page.waitForSelector('#continue'))
                      .then(() => page.click('#continue'))
                      .then(() => {
                        console.log('Clicked on "Continue" button.');
                      })
                      .then(() => page.waitForSelector('#finish'))
                      .then(() => page.$eval('#finish', el => el.textContent))
                      .then(finishButtonText => {
                        // Wait for the "Finish" button
                        if (finishButtonText.includes('Finish')) {
                          console.log('Finish button text validation passed.');
                        } else {
                          console.log('Finish button text validation failed.');
                        }
                      })
                      .then(() => page.waitForSelector('#finish'))
                      .then(() => page.click('#finish'))
                      .then(() => {
                        console.log('Clicked on "Finish" button.');
                      })
                      .then(() => page.waitForSelector('.complete-header'))
                      .then(() => page.$eval('.complete-header', el => el.textContent))
                      .then(thankYouText => {
                        // Wait for the "Thank you for your order!" text
                        if (thankYouText.includes('Thank you for your order!')) {
                          console.log('Thank you text validation passed.');
                        } else {
                          console.log('Thank you text validation failed.');
                        }
                      })
                      .then(() => page.waitForSelector('#back-to-products'))
                      .then(() => page.click('#back-to-products'))
                      .then(() => {
                        console.log('Clicked on "Back Home" button.');
                      })
                      .then(() => page.waitForSelector('.title'))
                      .then(() => page.$eval('.title', el => el.textContent))
                      .then(productsHeaderText => {
                        // Validate the "Products" text on the inventory page again
                        if (productsHeaderText.includes('Products')) {
                          console.log('Products text validation passed.');
                        } else {
                          console.log('Products text validation failed.');
                        }
                      })
                      .then(() => {
                        console.log('Script execution completed.');
                      })
                      .then(() => browser.close())
                      .catch(err => {
                        console.error('Error occurred:', err);
                      });
                  } else {
                    console.log('"Sauce Labs Onesie" not found.');
                    return browser.close();
                  }
                });
            });
        });
    }))
  .catch(err => {
    console.error('Error occurred:', err);
  });
