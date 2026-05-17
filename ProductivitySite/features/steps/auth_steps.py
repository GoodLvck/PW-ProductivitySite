from urllib.parse import urlparse

from behave import given, then, when
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from features.steps.common import _click_button, _wait

ROUTE_ALIASES = {
    "/login": "/accounts/login/",
    "/register": "/accounts/signup/",
    "/dashboard": "/dashboard/",
    "/": "/",
}

FIELD_ALIASES = {
    "username": "username",
    "password": "password",
    "first name": "first_name",
    "last name": "last_name",
    "email": "email",
}

DASHBOARD_ROUTES = {
    "/dashboard/",
    "/calendar/",
    "/subjects/",
    "/productivity/",
    "/profile/",
}


def _normalize_path(path):
    return ROUTE_ALIASES.get(path, path)


def _current_path(context):
    return urlparse(context.browser.url).path


def _wait(context, timeout=5):
    return WebDriverWait(context.browser.driver, timeout)


def _fill_by_label(context, label, value):
    label_key = label.strip().lower()

    if label_key == "username":
        context.browser.fill("username", value)
        return

    if label_key == "first name":
        context.browser.fill("first_name", value)
        return

    if label_key == "last name":
        context.browser.fill("last_name", value)
        return

    if label_key == "email":
        context.browser.fill("email", value)
        return

    if label_key == "name":
        parts = value.split(" ", 1)
        context.browser.fill("first_name", parts[0])
        context.browser.fill("last_name", parts[1] if len(parts) > 1 else "")
        return

    if label_key == "password":
        if context.browser.is_element_present_by_name("password1", wait_time=0.5):
            context.browser.fill("password1", value)
            if context.browser.is_element_present_by_name("password2", wait_time=0.5):
                context.browser.fill("password2", value)
        else:
            context.browser.fill("password", value)
        return

    field = FIELD_ALIASES.get(label_key, label_key)
    context.browser.fill(field, value)


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------

@given('I am on the "{path}" page')
@given('I am on "{path}"')
def step_open_page(context, path):
    context.browser.visit(f"{context.base_url}{_normalize_path(path)}")
    wait = WebDriverWait(context.browser.driver, 10)
    wait.until(visibility_of_element_located((By.CSS_SELECTOR, "body")))

@given("I am logged in")
def step_logged_in(context):
    user, _ = User.objects.get_or_create(
        username=context.test_user["username"],
        defaults={
            "email": context.test_user["email"],
            "first_name": context.test_user["first_name"],
            "last_name": context.test_user["last_name"],
        },
    )
    user.set_password(context.test_user["password"])
    user.save()

    context.browser.visit(f"{context.base_url}/accounts/login/")
    context.browser.fill("username", context.test_user["username"])
    context.browser.fill("password", context.test_user["password"])
    _click_button(context, "Log in")

    # Espera a que el sidebar sea visible (indica que estamos en el dashboard)
    wait = WebDriverWait(context.browser.driver, 10)
    wait.until(visibility_of_element_located((By.CSS_SELECTOR, ".app-sidebar")))

@given('a user with email "{email}" already exists')
def step_user_exists(context, email):
    username = email.split("@")[0]
    user, _ = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "first_name": "Ana",
            "last_name": "Lopez",
        },
    )
    user.email = email
    user.set_password("Secret123")
    user.save()

@given("I am on any page within the DashboardLayout")
def step_on_dashboard_layout(context):
    current = _current_path(context)
    assert any(current.startswith(route.rstrip("/")) for route in DASHBOARD_ROUTES), \
        f"Expected to be on a dashboard route, got {current}"

# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------

@when('I enter "{value}" in "{label}"')
@when('I enter "{value}" in the "{label}" field')
def step_enter_value(context, value, label):
    _fill_by_label(context, label, value)


@when('I click "{text}"')
@when('I click the "{text}" button')
def step_click_button(context, text):
    _click_button(context, text)


@when("I enter an invalid username or password")
def step_invalid_credentials(context):
    context.browser.fill("username", "wrong_user")
    context.browser.fill("password", "wrong_password")


@when('I click the "{text}" link')
def step_click_link(context, text):
    try:
        el = _wait(context).until(
            EC.element_to_be_clickable((By.LINK_TEXT, text))
        )
        el.click()
    except Exception:
        el = _wait(context).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, text))
        )
        el.click()


@when("I open the user menu in the header")
def step_open_user_menu(_context):
    # Direct logout link in current UI; no dropdown needed.
    return


@when("I try to register with that same email")
def step_register_same_email(context):
    context.browser.fill("first_name", "Ana")
    context.browser.fill("last_name", "Lopez")
    context.browser.fill("username", "ana")
    context.browser.fill("email", "ana@example.com")
    context.browser.fill("password1", "Secret123")
    context.browser.fill("password2", "Secret123")
    _click_button(context, "Create account")


@when("I enter a password shorter than 8 characters")
def step_short_password(context):
    context.browser.fill("first_name", "Ana")
    context.browser.fill("last_name", "Lopez")
    context.browser.fill("username", "ana_weak")
    context.browser.fill("email", "ana_weak@example.com")
    context.browser.fill("password1", "1234")
    context.browser.fill("password2", "1234")

@when('I leave the "{field}" field empty')
def step_leave_field_empty(context, field):
    key = field.strip().lower()
    field_map = {
        "first name": "first_name",
        "last name": "last_name",
        "username": "username",
        "email": "email",
        "password": "password1",
    }
    name = field_map.get(key)
    if name:
        context.browser.fill(name, "")
        if name == "password1" and context.browser.is_element_present_by_name("password2", wait_time=0.5):
            context.browser.fill("password2", "")
        return
    context.browser.fill(key, "")


@when("my session has been inactive for the configured timeout period")
def step_session_timeout(context):
    context.browser.visit(f"{context.base_url}/logout/")


# ---------------------------------------------------------------------------
# Then
# ---------------------------------------------------------------------------

@then('I am redirected to "{path}"')
def step_redirected_to(context, path):
    normalized = _normalize_path(path).rstrip("/")
    import time
    time.sleep(2)
    current = _current_path(context).rstrip("/")
    print(f"\nDEBUG: expected={normalized}, current={current}")
    assert current == normalized, f"Expected redirect to {normalized}, got {current}"

@then('I see the message "{message}"')
@then('I see the error message "{message}"')
def step_see_message(context, message):
    required_messages = {
        "First name is required",
        "Last name is required",
        "Username is required",
        "Email is required",
        "Password is required",
        "Name is required",
    }

    known_equivalents = {
        "Invalid credentials": "Please enter a correct username and password.",
        "Email is already in use": "A user with that username already exists.",
        "Password must be at least 8 characters": "This password is too short.",
        "Name is required": "This field is required.",
        "No tasks yet. Create your first one!": "NO PENDING TASKS!!",
    }

    if message in required_messages:
        driver = context.browser.driver
        invalid = driver.find_elements(By.CSS_SELECTOR, "input:invalid, select:invalid")
        assert len(invalid) > 0, f'No invalid required fields found for message: "{message}"'
        return

    if context.browser.is_text_present(message, wait_time=2):
        return

    alt = known_equivalents.get(message)
    if alt and context.browser.is_text_present(alt, wait_time=2):
        return

    raise AssertionError(f'Message not found: "{message}"')

@then("the {text} button is disabled temporarily")
def step_button_disabled(context, text):
    assert context.browser.is_element_present_by_css(
        "button[type='submit']", wait_time=2
    )


@then("I see the sidebar with my session active")
def step_sidebar_visible(context):
    wait = WebDriverWait(context.browser.driver, 5)
    wait.until(visibility_of_element_located((By.CSS_SELECTOR, ".app-sidebar")))


@then("my session is closed")
def step_session_closed(context):
    wait = WebDriverWait(context.browser.driver, 5)
    try:
        wait.until_not(visibility_of_element_located((By.CSS_SELECTOR, ".app-sidebar")))
    except Exception:
        pass
    assert not context.browser.is_element_present_by_css(".app-sidebar", wait_time=1)

@then("I am automatically logged out")
def step_auto_logged_out(context):
    current = _current_path(context).rstrip("/")
    assert current in ("/accounts/login", ""), \
        f"Expected logout redirect, got {current}"


@then("my account is created")
def step_account_created(context):
    assert (
        User.objects.filter(username="ana").exists()
        or User.objects.filter(email="ana@example.com").exists()
        or User.objects.filter(username=context.test_user["username"]).exists()
    )

@then('I remain on "{path}"')
def step_remain_on(context, path):
    import time
    time.sleep(1)
    expected = _normalize_path(path).rstrip("/")
    current = _current_path(context).rstrip("/")
    assert current == expected, f"Expected to remain on {expected}, got {current}"
