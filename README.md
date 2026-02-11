# QA Brains - Playwright Test Suite

This repository contains example regression and smoke tests for the login page at [https://practice.qabrains.com/ecommerce/login](https://practice.qabrains.com/ecommerce/login).

The test suite includes:
- **Smoke tests**: Quick critical path validations
- **Regression tests**: Comprehensive functionality and edge case testing
- Security tests for login functionality

## Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv env

# Activate virtual environment
# On Linux/Mac:
source env/bin/activate

# On Windows:
env\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install required packages
pip install playwright pytest python-dotenv

# Install Playwright browsers
playwright install
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
# Quick smoke run (before commit)
pytest -m smoke

# Full regression run (on PR/merge)
pytest -m regression

# Run all tests
pytest

# Run specific test file
pytest tests/e-comerce/test_login.py

# Run with verbose output
pytest -v
```

## Test Structure

- `tests/e-comerce/test_login.py` - Login page test suite
- `conftest.py` - Pytest configuration and fixtures
- `pytest.ini` - Pytest markers configuration
