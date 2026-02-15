from dotenv import load_dotenv
import pytest
from playwright.sync_api import Page

# NOTE:used for local setup only. For CI/CD, we use environment variables.
load_dotenv()


@pytest.fixture(scope="function")
def setup_page(page: Page):
    """Fixture to navigate to the e-commerce login page"""
    page.goto("https://practice.qabrains.com/ecommerce/login", timeout=30000)
    page.get_by_role("heading", name="Login").wait_for(state="visible", timeout=30000)
    yield page
