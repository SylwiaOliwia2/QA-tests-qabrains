from playwright.sync_api import Page, expect
import os
import re
import uuid

def check_user_has_logged_in(page: Page, filename: str = f"{uuid.uuid4().hex}.png"):
    """Helper function to verify user has successfully logged in"""
    expect(page).to_have_url(re.compile(".*ecommerce"), timeout=30000)
    try:
        expect(page.get_by_role("heading", name="Products")).to_be_visible(timeout=30000)
    except Exception:
        page.screenshot(path=filename, full_page=True)
        expect(page.get_by_role("heading", name="Products")).to_be_visible(timeout=1)


def log_in_user(page: Page, email: str = os.getenv("EMAIL"), password: str = os.getenv("PASSWORD")):
    """Helper function to log in user"""
    page.get_by_label("Email").fill(email)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Login").click()
