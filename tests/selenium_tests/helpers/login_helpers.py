import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fill_email_field(driver_login_page, email: str = os.getenv("EMAIL")):
    email_field = driver_login_page.find_element(by=By.ID, value="email")
    email_field.send_keys(email)
    return email_field

def fill_password_field(driver_login_page, password: str = os.getenv("PASSWORD")):
    password_field = driver_login_page.find_element(by=By.ID, value="password")
    password_field.send_keys(password)
    return password_field

def check_user_has_logged_in(driver_login_page):
    wait = WebDriverWait(driver_login_page, 10)
    header = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert header.text.strip() == "Products"
    
    current_url = driver_login_page.current_url
    assert "login" not in current_url.lower()

def log_in_user(driver_login_page, email: str = os.getenv("EMAIL"), password: str = os.getenv("PASSWORD")):
    email_field = fill_email_field(driver_login_page, email)
    password_field = fill_password_field(driver_login_page, password)
    login_button = driver_login_page.find_element(by=By.CSS_SELECTOR, value="button.btn-submit")
    login_button.click()