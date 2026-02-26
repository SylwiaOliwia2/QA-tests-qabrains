from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pytest
from tests.selenium_tests.helpers.login_helpers import fill_email_field, fill_password_field, check_user_has_logged_in, log_in_user


@pytest.mark.smoke
def test_login_title(driver_login_page):
    title = driver_login_page.title
    assert title == "QA Practice Site"


@pytest.mark.smoke
def test_user_can_log_in_with_valid_credentials(driver_login_page):
    log_in_user(driver_login_page)
    check_user_has_logged_in(driver_login_page)


@pytest.mark.smoke
def test_user_can_log_in_with_valid_credentials_2(driver_login_page):
    email_field = fill_email_field(driver_login_page)
    password_field = fill_password_field(driver_login_page)

    # press enter
    password_field.send_keys(u'\ue007')

    check_user_has_logged_in(driver_login_page)


@pytest.mark.smoke
@pytest.mark.regression
def test_user_sees_error_message_when_password_is_invalid(driver_login_page):
    log_in_user(driver_login_page, password="some_password_123")

    driver_login_page.implicitly_wait(5)
    warning = driver_login_page.find_element(
        By.XPATH, "//p[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'password is incorrect')]"
    )
    assert warning.is_displayed()


@pytest.mark.smoke
@pytest.mark.regression
def test_user_sees_error_message_when_email_is_incorrect(driver_login_page):
    log_in_user(driver_login_page, "xsfsfsfdx@gmail.com")

    driver_login_page.implicitly_wait(5)
    warning = driver_login_page.find_element(
        By.XPATH, "//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'password matched but email is incorrect')]"
    )
    assert warning.is_displayed()


@pytest.mark.regression
def test_password_is_masked(driver_login_page):
    password_field = fill_password_field(driver_login_page)

    assert password_field.get_attribute("type") == "password"


@pytest.mark.regression
def test_password_can_be_unmasked(driver_login_page):
    password_field = fill_password_field(driver_login_page, "password1234")
    
    toggle_button = driver_login_page.find_element(
        By.XPATH,
        "//div[contains(@class, 'form-field-group') and .//input[@id='password']]//button"
    )
    toggle_button.click()
    
    assert password_field.get_attribute("type") == "text"


@pytest.mark.regression
def test_user_sees_error_message_when_email_or_password_is_missing(driver_login_page):
    missing_email_text = "Email is a required field"
    missing_password_text = "Password is a required field"

    login_button = driver_login_page.find_element(by=By.CSS_SELECTOR, value="button.btn-submit")
    login_button.click()

    driver_login_page.implicitly_wait(5)

    email_warning = driver_login_page.find_element(
        By.XPATH, f"//p[contains(text(), '{missing_email_text}')]"
    )
    assert email_warning.is_displayed()

    password_warning = driver_login_page.find_element(
        By.XPATH, f"//p[contains(text(), '{missing_password_text}')]"
    )
    assert password_warning.is_displayed()


@pytest.mark.regression
def test_whitespaces_are_trimmed_from_email(driver_login_page):
    email_text = "    " + os.getenv("EMAIL") + " "
    
    log_in_user(driver_login_page, email_text)
    check_user_has_logged_in(driver_login_page)


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.current
def test_logged_in_user_can_log_out(driver_login_page):
    log_in_user(driver_login_page)

    driver_login_page.implicitly_wait(5)
    
    dropdown_menu = driver_login_page.find_element(By.CSS_SELECTOR, '[data-slot="dropdown-menu-trigger"]')
    dropdown_menu.click()

    logout_button = driver_login_page.find_element(
        By.XPATH,
        "//button[@data-slot='dialog-trigger' and .//div[text()[normalize-space()='Log out']]]"
    )
    logout_button.click()

    confirm_logout_button = driver_login_page.find_element(
        By.XPATH,
        "//button[@data-slot='dialog-close' and contains(@class,'bg-red-500') and normalize-space(text())='Logout']"
    )
    confirm_logout_button.click()

    login_url = "https://practice.qabrains.com/ecommerce/login"
    
    # NOTE: if wait.until will be updated to use `find_element`, it will interfere with `implicitly_wait`. Consider using `WebDriverWait` instead of `implicitly_wait`.
    wait = WebDriverWait(driver_login_page, 10)
    wait.until(lambda driver: driver.current_url == login_url)

    assert driver_login_page.current_url == login_url
    assert driver_login_page.title == "QA Practice Site"

