from playwright.sync_api import Page, expect
import pytest
import os
import re

from tests.helpers.login_helpers import check_user_has_logged_in, log_in_user


@pytest.mark.smoke
def test_has_heading(page: Page, setup_page):
    expect(
        page.get_by_role("heading", name="Login")
    ).to_be_visible()


@pytest.mark.smoke
@pytest.mark.regression
def test_user_can_log_in_with_valid_credentials(page: Page, setup_page):
    page.get_by_label("Email").fill(os.getenv("EMAIL"))
    page.get_by_label("Password").fill(os.getenv("PASSWORD"))
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(re.compile(".*ecommerce"), timeout=30000)
    try:
        expect(page.get_by_role("heading", name="Products")).to_be_visible(timeout=30000)
    except Exception:
        page.screenshot(path="debug.png", full_page=True)
        expect(page.get_by_role("heading", name="Products")).to_be_visible(timeout=1)


@pytest.mark.regression
def test_user_can_log_in_with_valid_credentials_2(page: Page, setup_page):

    page.get_by_label("Email").fill(os.getenv("EMAIL"))

    password = page.get_by_label("Password")
    password.fill(os.getenv("PASSWORD"))

    # Wait for navigation after pressing Enter - CI environments are slower
    with page.expect_navigation(timeout=60000, wait_until="networkidle"):
        password.press("Enter")

    check_user_has_logged_in(page)


@pytest.mark.smoke
@pytest.mark.regression
def test_user_sees_error_message_when_password_is_invalid(page: Page, setup_page):
    page.get_by_label("Email").fill(os.getenv("EMAIL"))
    page.get_by_label("Password").fill("invalid")

    page.get_by_role("button", name="Login").click()

    password_warning = page.get_by_text("Username matched but password is incorrect.")
    expect(password_warning).to_be_visible()


@pytest.mark.smoke
@pytest.mark.regression
def test_user_sees_error_message_when_email_is_incorrect(page: Page, setup_page):
    page.get_by_label("Email").fill("xsfsfsfdx@gmail.com")
    page.get_by_label("Password").fill(os.getenv("PASSWORD"))

    page.get_by_role("button", name="Login").click()

    expect(page.get_by_text("Password matched but email is incorrect.")).to_be_visible()


@pytest.mark.regression
def test_password_is_masked(page: Page, setup_page):
    password_value = "qwerty123"

    password = page.get_by_label("Password")
    password.fill(password_value)
    expect(password).to_have_attribute("type", "password")
    expect(password).to_have_value(password_value)


@pytest.mark.regression
@pytest.mark.fragile
def test_password_can_be_unmasked(page: Page, setup_page):
    password_value = "qwerty123"

    password = page.get_by_label("Password")
    password.fill(password_value)
    
    # NOTE:Find button in the same container as password field
    # The button has no id, so it's hard to identify it in different way
    # If problematic in future test, consider to not test it at all
    toggle_button = password.locator("xpath=ancestor::*[contains(@class, 'relative') or contains(@class, 'password')]//button")

    toggle_button.click()
    
    expect(password).to_have_attribute("type", "text")
    expect(password).to_have_value(password_value)


@pytest.mark.regression
def test_user_sees_error_message_when_email_or_password_is_missing(page: Page, setup_page):
    missing_email_text = "Email is a required field"
    missing_password_text = "Password is a required field"

    expect(page.get_by_text(missing_email_text)).not_to_be_visible()
    expect(page.get_by_text(missing_password_text)).not_to_be_visible()

    page.get_by_role("button", name="Login").click()

    expect(page.get_by_text(missing_email_text)).to_be_visible()
    expect(page.get_by_text(missing_password_text)).to_be_visible()


@pytest.mark.regression
def test_whitespaces_are_trimmed_from_email(page: Page, setup_page):
    email_text = "    " + os.getenv("EMAIL") + ""
    
    log_in_user(page, email_text)    
    check_user_has_logged_in(page)


@pytest.mark.regression
@pytest.mark.smoke
def test_logged_in_user_can_log_out(page: Page, setup_page):
    log_in_user(page)
    
    page.get_by_role("button", name=os.getenv("EMAIL")).click()
    page.get_by_role("button", name="Log out").click()
    page.get_by_role("button", name="Logout").click()

    expect(page).to_have_url(re.compile(".*login"), timeout=30000)
    expect(page.get_by_role("heading", name="Login")).to_be_visible()
