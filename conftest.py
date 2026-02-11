from dotenv import load_dotenv
import pytest
from playwright.sync_api import Page

# NOTE:used for local setup only. For CI/CD, we use environment variables.
load_dotenv()


@pytest.fixture
def setup_page(page: Page):
    """Fixture to navigate to the e-commerce login page"""
    page.goto("https://practice.qabrains.com/ecommerce/login")
    yield
