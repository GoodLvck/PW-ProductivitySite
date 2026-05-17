from urllib.parse import urlparse

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

from features.steps.common import _click_button, _wait


ROUTE_ALIASES = {
    "/dashboard": "/dashboard/",
    "/subjects": "/subjects/",
    "/calendar": "/calendar/",
    "/productivity": "/productivity/",
    "/profile": "/profile/",
}


def _current_path(context):
    return urlparse(context.browser.url).path


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------

@given("the app is in light mode")
def step_app_in_light_mode(context):
    driver = context.browser.driver
    driver.execute_script("localStorage.setItem('theme', 'light');")
    driver.execute_script("document.documentElement.removeAttribute('data-theme');")


@given("the app is in dark mode")
def step_app_in_dark_mode(context):
    driver = context.browser.driver
    driver.execute_script("localStorage.setItem('theme', 'dark');")
    driver.execute_script("document.documentElement.setAttribute('data-theme', 'dark');")


@given("I have set the theme to dark mode")
def step_set_theme_dark(context):
    driver = context.browser.driver
    driver.execute_script("localStorage.setItem('theme', 'dark');")
    driver.execute_script("document.documentElement.setAttribute('data-theme', 'dark');")


# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------

@when('I click "{item}" in the sidebar')
def step_click_sidebar_item(context, item):
    el = _wait(context).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class,'sidebar')]//a[.//span[normalize-space(text())='{item}']]")
        )
    )
    el.click()


@when("I click the sidebar toggle")
def step_click_sidebar_toggle(context):
    el = _wait(context).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#sidebar-collapse-button"))
    )
    el.click()


@when("I click it again")
def step_click_sidebar_toggle_again(context):
    el = _wait(context).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#sidebar-collapse-button"))
    )
    el.click()


@when("I click the theme button in the header")
def step_click_theme_button(context):
    el = _wait(context).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#theme-toggle"))
    )
    el.click()


@when("I click the theme button")
def step_click_theme_button_generic(context):
    el = _wait(context).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#theme-toggle"))
    )
    el.click()


@when("I log out and log back in")
def step_logout_and_login(context):
    context.browser.visit(f"{context.base_url}/logout/")
    context.browser.visit(f"{context.base_url}/accounts/login/")
    context.browser.fill("username", context.test_user["username"])
    context.browser.fill("password", context.test_user["password"])
    _click_button(context, "Log in")
    _wait(context).until(
        visibility_of_element_located((By.CSS_SELECTOR, ".app-sidebar"))
    )


# ---------------------------------------------------------------------------
# Then
# ---------------------------------------------------------------------------

@then('the "{item}" item is highlighted as active')
def step_sidebar_item_active(context, item):
    el = _wait(context).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class,'sidebar')]//a[contains(@class,'is-active')][.//span[normalize-space(text())='{item}']]")
        )
    )
    assert el is not None, f'Sidebar item "{item}" is not highlighted as active'


@then("the sidebar collapses showing only icons")
def step_sidebar_collapsed(context):
    driver = context.browser.driver
    _wait(context).until(
        lambda d: "sidebar-collapsed" in d.find_element(By.CSS_SELECTOR, ".app-layout").get_attribute("class")
    )

@then("the sidebar expands showing icons and labels")
def step_sidebar_expanded(context):
    driver = context.browser.driver
    _wait(context).until(
        lambda d: "sidebar-collapsed" not in d.find_element(By.CSS_SELECTOR, ".app-layout").get_attribute("class")
    )

@then("the app switches to dark mode")
def step_app_dark_mode(context):
    driver = context.browser.driver
    theme = driver.execute_script(
        "return document.documentElement.getAttribute('data-theme');"
    )
    assert theme == "dark", f"Expected dark mode, got {theme}"


@then("the preference is preserved on page reload")
def step_preference_preserved(context):
    driver = context.browser.driver
    driver.refresh()
    _wait(context).until(
        visibility_of_element_located((By.CSS_SELECTOR, ".app-sidebar"))
    )
    theme = driver.execute_script(
        "return document.documentElement.getAttribute('data-theme');"
    )
    assert theme == "dark", f"Expected dark mode after reload, got {theme}"


@then("the app returns to light mode")
def step_app_light_mode(context):
    driver = context.browser.driver
    theme = driver.execute_script(
        "return document.documentElement.getAttribute('data-theme');"
    )
    assert theme != "dark", f"Expected light mode, got {theme}"


@then("the app loads in dark mode")
def step_app_loads_dark(context):
    driver = context.browser.driver
    theme = driver.execute_script(
        "return document.documentElement.getAttribute('data-theme');"
    )
    assert theme == "dark", f"Expected dark mode after login, got {theme}"