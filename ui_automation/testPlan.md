# Test Plan

## Project Name:
Automated Web Application Testing for Swag Labs (https://www.saucedemo.com/)

## Prepared By:
Nav Durg Raman Pratap Singh

## Version:
1.0

## Date:
Sep 1, 2024

## 1. Introduction

This test plan outlines the strategy and approach for testing the web application [Swag Labs](https://www.saucedemo.com/) using Selenium WebDriver. The primary goal is to ensure that the login process, product selection, cart operations, checkout process, and logout functionality work as expected.

## 2. Objectives

- To validate that users can log in successfully using valid credentials.
- To verify that the correct product can be selected and added to the shopping cart.
- To ensure that the checkout process is functioning correctly.
- To confirm that users can log out successfully.

## 3. Scope

- **In-Scope:**
  - Testing the login functionality with valid credentials.
  - Testing the product selection and adding the product to the cart.
  - Testing the checkout process including form submission.
  - Testing the logout functionality.

- **Out-of-Scope:**
  - Performance testing of the application.
  - Testing of invalid or edge case scenarios (e.g., incorrect login credentials).
  - Cross-browser testing (only Chrome is tested).

## 4. Test Environment

- **Browser:** Google Chrome
- **WebDriver:** Selenium WebDriver
- **Operating System:** [Your OS, e.g., Windows 10, macOS]
- **Test URL:** [https://www.saucedemo.com/](https://www.saucedemo.com/)

## 5. Assumptions

- The test environment is stable and the website is accessible.
- The Chrome WebDriver is compatible with the installed Chrome browser version.
- Environment variables `USERNAME` and `PASSWORD` are correctly set up.

## 6. Test Cases

| **Test Case ID** | **Test Case Description**                                                | **Preconditions**                                     | **Test Steps**                                                                                                                                           | **Expected Result**                                                                                                                                              | **Status** |
|------------------|------------------------------------------------------------------------|------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| TC01             | Validate the logo text contains 'Swag Labs'                            | The Swag Labs website is accessible.                 | 1. Navigate to the login page. <br>2. Verify the logo text.                                                                                                | The logo text should contain 'Swag Labs'.                                                                                                                       | Pass/Fail  |
| TC02             | Validate successful login with valid credentials                       | Valid credentials are available in environment vars. | 1. Enter username and password. <br>2. Click the login button.                                                                                            | The user should be redirected to the Products page, and the title should contain 'Products'.                                                                     | Pass/Fail  |
| TC03             | Validate product selection and add to cart                             | User is logged in.                                   | 1. Click on 'Sauce Labs Onesie'. <br>2. Verify the product name and price. <br>3. Add the product to the cart. <br>4. Validate the product is in the cart. | The product name and price should be correct. The product should be successfully added to the cart and appear in the cart items list.                            | Pass/Fail  |
| TC04             | Validate the checkout process                                          | Product is added to the cart.                        | 1. Click on the cart link. <br>2. Click 'Checkout'. <br>3. Enter checkout info. <br>4. Continue and finish the checkout.                                  | The user should be able to enter their information, continue, and finish the checkout process. A 'Thank you' message should appear after the order is completed. | Pass/Fail  |
| TC05             | Validate logout functionality                                          | User is logged in.                                   | 1. Click on the menu button. <br>2. Click 'Logout'. <br>3. Verify the login button appears.                                                                | The user should be successfully logged out, and the login page should be displayed.                                                                              | Pass/Fail  |

## 7. Exit Criteria

- All critical test cases have passed.
- Any identified defects have been addressed or documented for future resolution.
- The application meets the acceptance criteria specified in the test cases.

## 8. Reporting

- Test results will be documented in a test summary report, including the status of each test case, any defects identified, and recommendations for improvements.

## 9. Risks and Mitigation

| **Risk**                                          | **Impact** | **Mitigation** |
|---------------------------------------------------|------------|----------------|
| The website is down or inaccessible.              | High       | Test will be rescheduled once the site is back online. |
| Environment variables are not set up correctly.   | Medium     | Ensure that the environment variables `USERNAME` and `PASSWORD` are set up before testing. |
| WebDriver compatibility issues.                   | Medium     | Update WebDriver to the latest version compatible with the installed Chrome browser. |

## 10. Approval

| **Name**         | **Title**           | **Signature** | **Date**        |
|------------------|---------------------|---------------|-----------------|
| Nav Durg R P Singh | Senior QA Engineer |               | Sep 1, 2024      |
