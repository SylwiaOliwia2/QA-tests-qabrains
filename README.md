# QA Brains - Test Suite

This repository contains example regression and smoke tests for the login page at [https://practice.qabrains.com/ecommerce/login](https://practice.qabrains.com/ecommerce/login), implemented in both **Playwright** and **Selenium**.

The test suite includes:
- **Smoke tests**: Quick critical path validations
- **Regression tests**: Comprehensive functionality and edge case testing
- Security tests for login functionality
- Tests implemented in both **Playwright** and **Selenium** frameworks

## Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv env

# Activate virtual environment
# On Linux/Mac:
source env/bin/activate
```

### 2. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Install Playwright browsers (for Playwright tests)
playwright install

# Chrome/ChromeDriver is required for Selenium tests (usually auto-installed)
```

### 3. Create .env File

Create a `.env` file in the root directory with your test credentials:

```bash
# .env file
EMAIL=your-email@example.com
PASSWORD=your-password
```

**Note**: The `.env` file is already in `.gitignore` to prevent committing credentials.

## Running Tests

```bash
# Quick smoke run (before commit) - runs both Playwright and Selenium
pytest -m smoke

# Full regression run (on PR/merge) - runs both frameworks
pytest -m regression

# Run all tests (both frameworks)
pytest

# Run only Playwright tests
pytest tests/playwright_tests/

# Run only Selenium tests
pytest tests/selenium_tests/

# Run specific test file
pytest tests/playwright_tests/e-commerce/test_login.py
pytest tests/selenium_tests/e-commerce/test_login_selenium.py

# Run with verbose output
pytest -v
```

## Test Structure

- `tests/playwright_tests/e-commerce` - Playwright test suite
- `tests/playwright_tests/helpers` - Helper functions for Playwright tests
- `tests/selenium_tests/e-commerce` - Selenium test suite
- `tests/selenium_tests/helpers` - Helper functions for Selenium tests
- `pytest.ini` - Pytest markers configuration

## CI/CD with GitHub Actions

This repository includes GitHub Actions workflows for automated testing.

### Setup GitHub Secrets

For CI/CD to work, you need to configure GitHub Secrets:

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions** → **Repository secrets**
3. Add the following secrets:
   - `EMAIL`: Your test account email
   - `PASSWORD`: Your test account password

### CI Workflow

The workflow (`.github/workflows/tests.yml`) runs:

- **Smoke tests**: On every push and pull request
  - Fast feedback on critical functionality
  - Blocks PRs if smoke tests fail
  - Runs separately for Playwright and Selenium frameworks

- **Regression tests**: Only on merge to `main`/`master`
  - Comprehensive test suite
  - Full validation before deployment
  - Runs separately for Playwright and Selenium frameworks

### Workflow Triggers

- `push` to `main`, `master`, or `develop` branches
- `pull_request` to `main`, `master`, or `develop` branches
