# Pytest API Testing Framework

This repository contains a framework for testing API endpoints using `pytest`. The framework supports JSON schema validation, logging, and report generation in HTML and JSON format using pytest plugins.

---

## Folder Structure

```plaintext
Pytest/
├── resources/                # JSON schemas for validating API responses
│   ├── comment_schema.json
│   ├── post_schema.json
│   └── user_schema.json
├── tests/                    # Test cases and fixtures
│   ├── conftest.py           # Shared test fixtures and configuration
│   ├── test_comments.py      # Tests for Comments API
│   ├── test_posts.py         # Tests for Posts API
│   └── test_users.py         # Tests for Users API
├── utils/                    # Utility functions (empty placeholder for now)
├── config.py                 # Configuration for base URL and headers
├── pytest.ini                # Pytest configuration file
├── requirements.txt          # Python dependencies
├── execution.log             # Execution logs for test runs
├── report.html               # HTML report generated by pytest-html
├── report.json               # JSON report generated by pytest-json-report
└── __init__.py               # Makes the directory a Python package

```
## Prerequisites

- **Python**: Version 3.x (check with `python --version`)
- **pip**: Package installer (check with `pip --version`)
- **pytest**: Install using `pip install pytest`

## Installation

1. Clone this repository:
    ```bash
    git clone <repository-url>
    ```

2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the tests with below command and monitor the .report.json file for complete report
    ```bash
    pytest -n auto -v --json-report
    ```