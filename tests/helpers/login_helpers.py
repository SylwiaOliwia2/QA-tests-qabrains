from playwright.sync_api import Page, expect
import os
import re


def check_user_has_logged_in(page: Page):
    """Helper function to verify user has successfully logged in"""
    # Wait for navigation to complete and page to be ready
    page.wait_for_load_state("networkidle", timeout=60000)
    expect(page).to_have_url(re.compile(".*ecommerce"), timeout=30000)


def log_in_user(page: Page, email: str = os.getenv("EMAIL"), password: str = os.getenv("PASSWORD")):
    """Helper function to log in user"""
    page.get_by_label("Email").fill(email)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Login").click()
