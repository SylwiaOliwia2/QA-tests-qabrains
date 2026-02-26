from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pytest


@pytest.mark.smoke
def test_login_title(driver_login_page):
    title = driver_login_page.title
    assert title == "QA Practice Site"


@pytest.mark.smoke
def test_user_can_log_in_with_valid_credentials(driver_login_page):
    email_field = driver_login_page.find_element(by=By.ID, value="email")
    email_field.clear()
    email_field.send_keys(os.getenv("EMAIL"))

    assert email_field.get_attribute("value") == os.getenv("EMAIL")
    
    password_field = driver_login_page.find_element(by=By.ID, value="password")
    password_field.clear()
    password_field.send_keys(os.getenv("PASSWORD"))
    
    assert password_field.get_attribute("value") == os.getenv("PASSWORD")
    
    submit_button = driver_login_page.find_element(by=By.CSS_SELECTOR, value="button.btn-submit")
    submit_button.click()
    
    wait = WebDriverWait(driver_login_page, 10)
    header = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert header.text.strip() == "Products"
    
    current_url = driver_login_page.current_url
    assert "login" not in current_url.lower()
