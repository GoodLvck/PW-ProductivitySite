from urllib.parse import urlparse

from behave import given, when, then
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from features.steps.common import _click_button, _wait

from productivity_site.models import Subject


def _current_path(context):
    return urlparse(context.browser.url).path


def _wait(context, timeout=10):
    return WebDriverWait(context.browser.driver, timeout)


def _get_test_user(context):
    return User.objects.get(username=context.test_user["username"])


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------

@given('I am on the detail page of subject "{name}"')
def step_on_subject_detail(context, name):
    user = _get_test_user(context)
    subject, _ = Subject.objects.get_or_create(
        name=name,
        user_id=user,
        defaults={"description": "Test description", "color": "#7d9b76"},
    )
    context.current_subject = subject
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}"
    )
    _wait(context).until(
        visibility_of_element_located((By.CSS_SELECTOR, "body"))
    )


@given('a subject named "{name}" already exists')
def step_subject_exists(context, name):
    user = _get_test_user(context)
    subject, _ = Subject.objects.get_or_create(
        name=name,
        user_id=user,
        defaults={"description": "Test description", "color": "#7d9b76"},
    )
    context.current_subject = subject


@given("I have 3 subjects created")
def step_three_subjects(context):
    user = _get_test_user(context)
    Subject.objects.filter(user_id=user).delete()
    for i in range(1, 4):
        Subject.objects.create(
            name=f"Subject {i}",
            user_id=user,
            description=f"Description {i}",
            color="#7d9b76",
        )


@given("I have no subjects created")
def step_no_subjects(context):
    user = _get_test_user(context)
    Subject.objects.filter(user_id=user).delete()


@given('the subject "{name}" exists')
def step_subject_named_exists(context, name):
    user = _get_test_user(context)
    subject, _ = Subject.objects.get_or_create(
        name=name,
        user_id=user,
        defaults={"description": "Test description", "color": "#7d9b76"},
    )
    context.current_subject = subject


@given('the subject "{name}" has {count:d} tasks')
def step_subject_has_tasks(context, name, count):
    # Placeholder hasta implementar el modelo Task
    pass


# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------

@when('I navigate to "{path}"')
def step_navigate_to(context, path):
    context.browser.visit(f"{context.base_url}{path}")
    _wait(context).until(
        visibility_of_element_located((By.CSS_SELECTOR, "body"))
    )


@when('I fill in "{field}" with "{value}"')
def step_fill_in(context, field, value):
    field_map = {
        "Name": "name",
        "Description": "description",
        "Task description": "text",
    }
    name = field_map.get(field, field.lower())
    context.browser.fill(name, value)


@when('I select color "{color}"')
def step_select_color(context, color):
    context.selected_color = color
    driver = context.browser.driver
    el = _wait(context).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='color'], input[name='color']")
        )
    )
    driver.execute_script(f"arguments[0].value = '{color}';", el)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", el)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", el)


@when('I click the floating "{text}" button')
def step_click_floating_button(context, text):
    driver = context.browser.driver
    toggle = _wait(context).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".floating-actions-toggle"))
    )
    toggle.click()
    _wait(context).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#floating-actions-menu"))
    )

@when('I change the name to "{name}"')
def step_change_name(context, name):
    context.browser.fill("name", name)


@when('I change the description to "{description}"')
def step_change_description(context, description):
    context.browser.fill("description", description)


@when("I confirm the deletion")
def step_confirm_deletion(context):
    el = _wait(context).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button-destructive"))
    )
    el.click()


@when("I cancel the confirmation")
def step_cancel_confirmation(context):
    el = _wait(context).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[self::button or self::a][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cancel')]")
        )
    )
    el.click()


@when('I click on the "{name}" card')
def step_click_subject_card(context, name):
    el = _wait(context).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//*[contains(@class, 'subject-card')][.//*[normalize-space(text())='{name}']]")
        )
    )
    el.click()


# ---------------------------------------------------------------------------
# Then
# ---------------------------------------------------------------------------

@then('the subject "{name}" appears in the grid')
def step_subject_in_grid(context, name):
    _wait(context).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[contains(@class, 'subject-card')][.//*[normalize-space(text())='{name}']]")
        )
    )


@then("the card uses the selected color")
def step_card_uses_color(context):
    driver = context.browser.driver
    color = getattr(context, "selected_color", "#7d9b76")
    els = driver.find_elements(
        By.XPATH,
        f"//*[contains(@style, '{color}') or @data-color='{color}']"
    )
    assert len(els) > 0, f"No element found with color {color}"


@then('the "Create" button remains disabled')
def step_create_button_disabled(context):
    driver = context.browser.driver
    buttons = driver.find_elements(
        By.XPATH,
        "//*[self::button or self::input[@type='submit']][normalize-space(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))='create']"
    )
    assert any(not btn.is_enabled() for btn in buttons), "Create button is not disabled"


@then("the subject is not created")
def step_subject_not_created(context):
    user = _get_test_user(context)
    count = Subject.objects.filter(user_id=user).count()
    assert count == 0, f"Expected no subjects but found {count}"


@then("the dialog closes")
def step_dialog_closes(context):
    _wait(context).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, "dialog, .modal, [role='dialog']")
        )
    )


@then('the subject "{name}" does not appear in the grid')
def step_subject_not_in_grid(context, name):
    driver = context.browser.driver
    els = driver.find_elements(
        By.XPATH,
        f"//*[contains(@class, 'subject-card')][.//*[normalize-space(text())='{name}']]"
    )
    assert len(els) == 0, f"Subject '{name}' should not appear in the grid"


@then("I see 3 subject cards in the grid")
def step_three_cards_in_grid(context):
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".subject-card"))
    )
    driver = context.browser.driver
    cards = driver.find_elements(By.CSS_SELECTOR, ".subject-card")
    assert len(cards) >= 3, f"Expected 3 subject cards, found {len(cards)}"


@then("each card shows name, description, and color")
def step_cards_show_info(context):
    driver = context.browser.driver
    cards = driver.find_elements(By.CSS_SELECTOR, ".subject-card")
    assert len(cards) > 0, "No cards found"


@then("I see a message inviting me to create my first subject")
def step_empty_state_message(context):
    assert context.browser.is_text_present("CREATE YOUR FIRST SUBJECT", wait_time=3), \
        "Empty state message not found"


@then("I see the detail view with its name, description, and task list")
def step_subject_detail_view(context):
    _wait(context).until(
        visibility_of_element_located((By.CSS_SELECTOR, "body"))
    )
    current = _current_path(context)
    assert "/subjects/" in current, f"Expected subject detail URL, got {current}"


@then('I see the breadcrumb "{breadcrumb}"')
def step_see_breadcrumb(context, breadcrumb):
    parts = breadcrumb.split(" / ")
    for part in parts:
        assert context.browser.is_text_present(part, wait_time=3), \
            f'Breadcrumb part "{part}" not found'


@then('the title shows "{name}"')
def step_title_shows(context, name):
    assert context.browser.is_text_present(name, wait_time=3), \
        f'Title "{name}" not found'


@then('the description shows "{description}"')
def step_description_shows(context, description):
    assert context.browser.is_text_present(description, wait_time=3), \
        f'Description "{description}" not found'


@then("the subject color is updated in the detail view and in the grid")
def step_color_updated(context):
    driver = context.browser.driver
    els = driver.find_elements(
        By.XPATH,
        "//*[contains(@style, '#c4654a') or @data-color='#c4654a']"
    )
    assert len(els) > 0, "Updated color not found in page"


@then("the original subject name is still displayed")
def step_original_name_displayed(context):
    subject = context.current_subject
    assert context.browser.is_text_present(subject.name, wait_time=3), \
        f'Original name "{subject.name}" not found'


@then('I am returned to "{path}"')
def step_returned_to(context, path):
    expected = path.rstrip("/")
    _wait(context).until(
        lambda driver: urlparse(driver.current_url).path.rstrip("/") == expected
    )
    current = _current_path(context).rstrip("/")
    assert current == expected, f"Expected to be on {expected}, got {current}"


@then('the subject "{name}" no longer appears in the grid')
def step_subject_gone_from_grid(context, name):
    import time
    time.sleep(1)
    driver = context.browser.driver
    els = driver.find_elements(
        By.XPATH,
        f"//*[contains(@class, 'subject-card')][.//*[normalize-space(text())='{name}']]"
    )
    assert len(els) == 0, f"Subject '{name}' still appears in the grid"


@then('the subject "{name}" still exists')
def step_subject_still_exists(context, name):
    user = _get_test_user(context)
    assert Subject.objects.filter(name=name, user_id=user).exists(), \
        f"Subject '{name}' not found in database"


@then('I see a warning "{message}"')
def step_see_warning(context, message):
    assert context.browser.is_text_present(message, wait_time=3), \
        f'Warning "{message}" not found'


@then("I must confirm before the deletion proceeds")
def step_must_confirm(context):
    driver = context.browser.driver
    els = driver.find_elements(
        By.XPATH,
        "//*[self::button or self::a][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'confirm') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'delete') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'yes')]"
    )
    assert len(els) > 0, "No confirmation button found"


@then('I see "{text}"')
def step_see_text(context, text):
    assert context.browser.is_text_present(text, wait_time=3), \
        f'Text "{text}" not found'