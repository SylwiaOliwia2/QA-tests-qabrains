from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest
import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# NOTE:used for local setup only. For CI/CD, we use environment variables.
load_dotenv()


def get_chrome_options():
    """Get Chrome options configured for both local and CI environments"""
    options = Options()
    
    # CI needs headless mode and other flags for stable run
    if os.getenv("CI") or os.getenv("GITHUB_ACTIONS"):
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
    
    return options


@pytest.fixture
def driver_login_page():
    options = get_chrome_options()
    driver = webdriver.Chrome(options=options)
    driver.get("https://practice.qabrains.com/ecommerce/login")
    yield driver
    driver.quit()