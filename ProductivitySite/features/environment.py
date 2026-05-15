import os
import re
import sys
import django

# ---------------------------------------------------------------------------
# Django setup – needed to access the ORM and create test fixtures
# ---------------------------------------------------------------------------
# Add the project root (where manage.py lives) to sys.path so that
# "ProductivitySite.settings" can be imported.
_FEATURES_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_FEATURES_DIR)  # …/ProductivitySite/
sys.path.insert(0, _PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProductivitySite.settings")
django.setup()

from django.contrib.auth.models import User  # noqa: E402 (imported after setup)
from splinter.browser import Browser  # noqa: E402

# ---------------------------------------------------------------------------
# Test-user credentials  (used by "Given I am logged in" and auth features)
# ---------------------------------------------------------------------------
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "first_name": "Test",
    "last_name": "User",
}

# Base URL of the running Django development server
BASE_URL = os.environ.get("TEST_SERVER_URL", "http://localhost:8000")


# ---------------------------------------------------------------------------
# Browser factories
# ---------------------------------------------------------------------------

def chrome_browser(headless=True):
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    return Browser("chrome", options=chrome_options)


def firefox_browser(headless=True):
    return Browser("firefox", headless=headless)


# ---------------------------------------------------------------------------
# Behave hooks
# ---------------------------------------------------------------------------

def before_all(context):
    context.browser = chrome_browser(headless=True)
    # Alternatively, use `firefox_browser` and headless=False to see the browser while testing
    context.base_url = BASE_URL
    context.test_user = TEST_USER

    # Ensure the test user exists in the database
    user, created = User.objects.get_or_create(
        username=TEST_USER["username"],
        defaults={
            "email": TEST_USER["email"],
            "first_name": TEST_USER["first_name"],
            "last_name": TEST_USER["last_name"],
        },
    )
    if created or not user.has_usable_password():
        user.set_password(TEST_USER["password"])
        user.save()


def after_all(context):
    context.browser.quit()
    context.browser = None


# ---------------------------------------------------------------------------
# Screenshot on step failure
# ---------------------------------------------------------------------------

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text)
    return text


def after_step(context, step):
    if step.status == "failed":
        feature = slugify(context.feature.name)
        scenario = slugify(context.scenario.name)
        step_name = slugify(step.name)
        os.makedirs("screenshots", exist_ok=True)
        filename = f"screenshots/{feature}__{scenario}__{step_name}.png"
        context.browser.driver.save_screenshot(filename)
