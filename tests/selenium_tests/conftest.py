from dotenv import load_dotenv
from selenium import webdriver
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# NOTE:used for local setup only. For CI/CD, we use environment variables.
load_dotenv()


@pytest.fixture
def driver_login_page():
    driver = webdriver.Chrome()
    driver.get("https://practice.qabrains.com/ecommerce/login")
    yield driver
    driver.quit()