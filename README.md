# SauceDemo Automation Test Suite

This project automates end-to-end tests for the [Sauce Demo](https://www.saucedemo.com/) application using **Selenium WebDriver** and **pytest**. The framework leverages the **Page Object Model (POM)** design pattern, making the tests **scalable, maintainable**, and **reusable** for dynamic web applications where UI elements change frequently.

## Features

- **Test Coverage**: Covers login, adding items to cart, checkout, and order placement.
- **Framework**: Utilizes pytest for test discovery, execution, and reporting.
- **Page Object Model (POM)**: Follows the POM design pattern to enhance code maintainability, scalability, and separation of concerns.
- **Scalable & Maintainable**: The codebase is designed to ensure minimal changes in test logic even when the UI changes, making it adaptable to frequent updates.
- **Environment Variables (Optional)**: Allows storing confidential information (e.g., Sauce Labs credentials) in a `.env` file.

## Prerequisites

- **Python**: Version 3.x (check with `python --version`)
- **pip**: Package installer (check with `pip --version`)
- **Selenium WebDriver**: Download the appropriate WebDriver for your browser from [Selenium WebDriver Downloads](https://www.selenium.dev/downloads/)
- **Web Browser**: Chrome, Firefox, or Edge are commonly used.
- **pytest**: Install using `pip install pytest`

**Optional**:
- **Sauce Labs Account (for browser testing)**: [Sign up here](https://saucelabs.com/sign-up)

## Installation

1. Clone this repository:
    ```bash
    git clone <repository-url>
    ```

2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

**Optional**:
- Create a `.env` file in the project root directory and set any necessary environment variables (e.g., `SAUCE_USERNAME`, `SAUCE_ACCESS_KEY`).

## Running Tests

1. Open your terminal in the project directory.
2. Run the tests with below command and monitor the TestsAutomationReport.html file for complete report
    ```bash
    pytest tests --html=TestsAutomationReport.html
    ```

**Optional (for Sauce Labs testing)**:
- Configure your Sauce Labs credentials in the environment variables or test configuration files.
- Follow [Sauce Labs documentation](https://docs.saucelabs.com/) for integrating with pytest.

> **Note**: Modify the path to your test files if they are not located in the default directory.



### 📁 **Directory Breakdown**

- **`pages/`**: Contains the Page Object classes, each representing a different page of the web application. This design pattern abstracts the locators and interactions, making the tests less prone to UI changes.
  
- **`tests/`**: Contains the test scripts written using `pytest`, covering different scenarios for [SauceDemo](https://www.saucedemo.com/). Each test file follows a clear structure to ensure readability and scalability.

- **`utils/`**: Includes utility modules to handle configurations, test data, and other reusable components, making the framework modular and easier to extend.

- **`conftest.py`**: Houses the shared `pytest` configurations and fixtures, ensuring a seamless and maintainable setup for the entire test suite.

## Test Structure

The test suite follows a clear structure with separate files for:

- **Page Objects**: Define locators and interactions for each page element (e.g., `LoginPage`, `InventoryPage`).
- **Test Cases**: Implement test logic using pytest functions (e.g., `test_login`, `test_add_to_cart`).

## Reporting

`pytest` automatically generates a test report in the terminal. For more detailed reports, you can use plugins like `pytest-html` to create HTML reports:
```bash
pip install pytest-html
pytest --html=report.html
