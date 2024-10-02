# SauceDemo Automation Test Suite

This project automates end-to-end tests for the Sauce Demo application using **Selenium WebDriver** and **pytest**.

## Features

- **Test Coverage**: Covers login, adding items to cart, checkout, and order placement.
- **Framework**: Utilizes pytest for test discovery, execution, and reporting.
- **Page Object Model (POM)**: Follows the POM design pattern to enhance code maintainability and separation of concerns.
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
2. Run the tests with:
    ```bash
    pytest
    ```

**Optional (for Sauce Labs testing)**:
- Configure your Sauce Labs credentials in the environment variables or test configuration files.
- Follow [Sauce Labs documentation](https://docs.saucelabs.com/) for integrating with pytest.

> **Note**: Modify the path to your test files if they are not located in the default directory.

## Test Structure

The test suite follows a clear structure with separate files for:

- **Page Objects**: Define locators and interactions for each page element (e.g., `LoginPage`, `InventoryPage`).
- **Test Cases**: Implement test logic using pytest functions (e.g., `test_login`, `test_add_to_cart`).

## Reporting

`pytest` automatically generates a test report in the terminal. For more detailed reports, you can use plugins like `pytest-html` to create HTML reports:
```bash
pip install pytest-html
pytest --html=report.html