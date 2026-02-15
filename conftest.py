from dotenv import load_dotenv
import pytest
from playwright.sync_api import Page, expect
import os
import re

# NOTE:used for local setup only. For CI/CD, we use environment variables.
load_dotenv()


@pytest.fixture(scope="function")
def setup_page(page: Page):
    """Fixture to navigate to the e-commerce login page"""
    page.goto("https://practice.qabrains.com/ecommerce/login", timeout=30000)
    page.get_by_role("heading", name="Login").wait_for(state="visible", timeout=30000)
    yield page

@pytest.fixture(scope="function")
def setup_shopping_page(page: Page):
    """
    Fixture to login to the shopping page
    It assumes, test_login.py passes.
    """
    page.goto("https://practice.qabrains.com/ecommerce/login", timeout=30000)
    page.get_by_label("Email").fill(os.getenv("EMAIL"))
    page.get_by_label("Password").fill(os.getenv("PASSWORD"))
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(re.compile(".*ecommerce"))
    yield page
