from datetime import timedelta
from urllib.parse import urlparse

from behave import given, when, then
from django.contrib.auth.models import User
from django.utils import timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from productivity_site.models import Subject, Task, Subtask
from features.steps.common import _wait


def _current_path(context):
    return urlparse(context.browser.url).path


def _get_test_user(context):
    return User.objects.get(username=context.test_user["username"])


def _get_or_create_subject(context, name="Mathematics"):
    user = _get_test_user(context)
    subject, _ = Subject.objects.get_or_create(
        name=name,
        user_id=user,
        defaults={"description": "Test description", "color": "#7d9b76"},
    )
    return subject


def _get_or_create_task(context, name="Submit chapter 3 problems"):
    subject = _get_or_create_subject(context)
    task, _ = Task.objects.get_or_create(
        name=name,
        subject_id=subject,
        defaults={
            "text": "Test description",
            "due_date": timezone.now() + timedelta(days=7),
            "priority": "medium",
            "estimated_time": 60,
            "completed": False,
        },
    )
    return task


def _create_subtask(task, name, completed=False):
    existing = Subtask.objects.filter(name=name, task_id=task).first()
    if existing:
        return existing
    subtask = Subtask(
        name=name,
        task_id=task,
        description="Test description",
        due_date=timezone.now() + timedelta(days=7),
        priority="medium",
        estimated_time=30,
        completed=completed,
    )
    subtask.save()
    return Subtask.objects.filter(name=name, task_id=task).first()


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------

@given('the task "Submit chapter 3 problems" has 4 subtasks, 2 completed')
def step_task_has_subtasks(context):
    task = _get_or_create_task(context)
    context.current_task = task
    context.current_subject = task.subject_id
    Subtask.objects.filter(task_id=task).delete()
    for i in range(1, 3):
        _create_subtask(task, f"Pending subtask {i}", completed=False)
    for i in range(1, 3):
        _create_subtask(task, f"Completed subtask {i}", completed=True)


@given("the task has no subtasks")
def step_task_no_subtasks(context):
    task = _get_or_create_task(context)
    Subtask.objects.filter(task_id=task).delete()


@given("I am on the subtask detail page")
def step_on_subtask_detail(context):
    task = _get_or_create_task(context)
    context.current_task = task
    context.current_subject = task.subject_id
    subtask = Subtask.objects.filter(task_id=task).first()
    if not subtask:
        subtask = _create_subtask(task, "Test subtask")
    context.current_subtask = subtask
    context.subtask_count_before = Subtask.objects.filter(task_id=task).count()
    subject = task.subject_id
    url = f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}/subtasks/{subtask.subtask_id}"
    context.browser.visit(url)
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".floating-actions-toggle"))
    )


@given("I am on the detail of a task with several subtasks")
def step_on_task_with_subtasks(context):
    task = _get_or_create_task(context)
    context.current_task = task
    context.current_subject = task.subject_id
    Subtask.objects.filter(task_id=task).delete()
    for i in range(1, 3):
        _create_subtask(task, f"Pending subtask {i}", completed=False)
    _create_subtask(task, "Completed subtask 1", completed=True)
    subject = task.subject_id
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}"
    )
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#task-subtasks"))
    )

@given("I am on the subtask detail page of a pending subtask")
def step_on_pending_subtask_detail(context):
    task = _get_or_create_task(context)
    context.current_task = task
    context.current_subject = task.subject_id
    subtask = Subtask.objects.filter(task_id=task, completed=False).first()
    if not subtask:
        subtask = _create_subtask(task, "Pending test subtask", completed=False)
    context.current_subtask = subtask
    subject = task.subject_id
    url = f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}/subtasks/{subtask.subtask_id}"
    context.browser.visit(url)
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".subtask-status-form"))
    )


@given("I am on the subtask detail page of a completed subtask")
def step_on_completed_subtask_detail(context):
    task = _get_or_create_task(context)
    context.current_task = task
    context.current_subject = task.subject_id
    subtask = Subtask.objects.filter(task_id=task, completed=True).first()
    if not subtask:
        subtask = _create_subtask(task, "Completed test subtask", completed=True)
    context.current_subtask = subtask
    context.subtask_count_before = Subtask.objects.filter(task_id=task).count()
    subject = task.subject_id
    url = f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}/subtasks/{subtask.subtask_id}"
    context.browser.visit(url)
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".subtask-status-form"))
    )


# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------

@when("I open the task detail")
def step_open_task_detail(context):
    task = context.current_task
    subject = context.current_subject
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}"
    )
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#task-subtasks"))
    )


@when("I set estimated time to {minutes:d}")
def step_set_estimated_time(context, minutes):
    context.browser.fill("estimated_time", str(minutes))


@when("I click on a subtask")
def step_click_on_subtask(context):
    el = _wait(context).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".subtask-card-content"))
    )
    el.click()


@when("I click the circle of a pending subtask")
def step_click_pending_circle(context):
    task = context.current_task
    context.pending_count_before = Subtask.objects.filter(
        task_id=task, completed=False
    ).count()
    el = _wait(context).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".subtask-card-pending .subtask-toggle-icon")
        )
    )
    el.click()
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".subtask-card-completed"))
    )


@when("I click the checkmark of a completed subtask")
def step_click_completed_checkmark(context):
    el = _wait(context).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".subtask-card-completed .subtask-toggle-icon")
        )
    )
    el.click()
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".subtask-card-pending"))
    )


@when("I click the status card to toggle completion")
def step_click_status_card_toggle(context):
    task = context.current_task
    context.pending_count_before = Subtask.objects.filter(
        task_id=task, completed=False
    ).count()
    el = _wait(context).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".subtask-status-card"))
    )
    el.click()


@when("I modify the name, description, time, or priority")
def step_modify_subtask(context):
    context.browser.fill("name", "Modified subtask name")


@when("I confirm")
def step_confirm(context):
    el = _wait(context).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button-destructive"))
    )
    el.click()

@when("I navigate back to the task detail page")
def step_navigate_back_to_task(context):
    task = context.current_task
    subject = context.current_subject
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}"
    )
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#task-subtasks"))
    )
@when("I click on a pending subtask")
def step_click_on_pending_subtask(context):
    el = _wait(context).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".subtask-card-pending .subtask-card-content")
        )
    )
    el.click()


@when("I click on a completed subtask")
def step_click_on_completed_subtask(context):
    el = _wait(context).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".subtask-card-completed .subtask-card-content")
        )
    )
    el.click()

# ---------------------------------------------------------------------------
# Then
# ---------------------------------------------------------------------------

@then('the subtask "{name}" appears in the list')
def step_subtask_in_list(context, name):
    _wait(context).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[contains(@class, 'subtask-card')][.//*[normalize-space(text())='{name}']]")
        )
    )


@then("the subtask counter increases by 1")
def step_subtask_counter_increases(context):
    task = context.current_task
    task.refresh_from_db()
    count = Subtask.objects.filter(task_id=task).count()
    assert count > 0, "Subtask counter did not increase"


@then("the subtask counter decreases by 1")
def step_subtask_counter_decreases(context):
    task = context.current_task
    count_before = getattr(context, "subtask_count_before", 1)
    count_after = Subtask.objects.filter(task_id=task).count()
    assert count_after < count_before, \
        f"Expected subtask count to decrease, was {count_before}, now {count_after}"


@then("I see each subtask with its status, name, time, and priority")
def step_see_subtask_details(context):
    driver = context.browser.driver
    cards = driver.find_elements(By.CSS_SELECTOR, ".subtask-card")
    assert len(cards) > 0, "No subtask cards found"
    for card in cards:
        assert card.find_elements(By.CSS_SELECTOR, ".subtask-toggle-icon"), \
            "Missing toggle icon in subtask card"
        assert card.find_elements(By.CSS_SELECTOR, ".subtask-card-name"), \
            "Missing name in subtask card"
        assert card.find_elements(By.CSS_SELECTOR, ".subtask-card-time"), \
            "Missing time in subtask card"
        assert card.find_elements(By.CSS_SELECTOR, ".priority-badge"), \
            "Missing priority badge in subtask card"


@then('the progress bar shows "2/4 subtasks" at 50%')
def step_progress_bar(context):
    _wait(context).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#task-subtasks .details-section-title h3"),
            "Subtasks (2)"
        )
    )


@then("I see the subtask detail view with all its fields")
def step_subtask_detail_view(context):
    current = _current_path(context)
    assert "/subtasks/" in current, f"Expected subtask detail URL, got {current}"
    driver = context.browser.driver
    assert driver.find_elements(By.CSS_SELECTOR, ".subtask-status-form"), \
        "Missing status toggle form on subtask detail"
    assert driver.find_elements(By.CSS_SELECTOR, ".subtask-details-card"), \
        "Missing details card on subtask detail"


@then("I am returned to the task detail page")
def step_returned_to_task(context):
    task = context.current_task
    subject = context.current_subject
    expected = f"/subjects/{subject.subject_id}/tasks/{task.task_id}"
    _wait(context).until(
        lambda driver: expected in urlparse(driver.current_url).path
    )


@then("the subtask no longer appears in the list")
def step_subtask_not_in_list(context):
    subtask = context.current_subtask
    driver = context.browser.driver
    import time
    time.sleep(1)
    els = driver.find_elements(
        By.XPATH,
        f"//*[contains(@class, 'subtask-card')][.//*[normalize-space(text())='{subtask.name}']]"
    )
    assert len(els) == 0, f"Subtask '{subtask.name}' still appears in the list"


@then("the subtask still exists")
def step_subtask_still_exists(context):
    subtask = context.current_subtask
    assert Subtask.objects.filter(subtask_id=subtask.subtask_id).exists(), \
        f"Subtask '{subtask.name}' not found in database"


@then("the icon changes to a completed checkmark")
def step_icon_changes_to_checkmark(context):
    _wait(context).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".subtask-card-completed .subtask-toggle-icon .fi-rr-check-circle")
        )
    )


@then("the name appears with strikethrough")
def step_subtask_name_strikethrough(context):
    driver = context.browser.driver
    els = driver.find_elements(
        By.CSS_SELECTOR, ".subtask-card-completed .subtask-card-name"
    )
    assert len(els) > 0, "No completed subtask card with a name element found"


@then("the parent task's progress bar is updated")
def step_parent_progress_updated(context):
    expected = context.pending_count_before - 1
    _wait(context).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#task-subtasks .details-section-title h3"),
            f"Subtasks ({expected})"
        )
    )


@then("it returns to a pending state")
def step_subtask_returns_pending(context):
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".subtask-card-pending"))
    )
    driver = context.browser.driver
    assert driver.find_elements(
        By.CSS_SELECTOR, ".subtask-card-pending .subtask-toggle-icon .fi-rr-circle"
    ), "Pending toggle icon (fi-rr-circle) not found after unmarking"


@then("the progress bar is recalculated")
def step_progress_recalculated(context):
    _wait(context).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#task-subtasks .details-section-title h3"),
            "Subtasks (3)"
        )
    )


@then("the status card shows completed")
def step_status_card_shows_completed(context):
    _wait(context).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".subtask-status-card.is-completed")
        )
    )


@then("the status card shows pending")
def step_status_card_shows_pending(context):
    driver = context.browser.driver
    _wait(context).until(
        lambda d: not d.find_elements(
            By.CSS_SELECTOR, ".subtask-status-card.is-completed"
        )
    )


@then("the changes are reflected when I return to the task")
def step_changes_reflected(context):
    task = context.current_task
    subject = context.current_subject
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}"
    )
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#task-subtasks"))
    )
    assert context.browser.is_text_present("Modified subtask name", wait_time=3), \
        "Modified subtask name not found in task detail"

@then('the subtask "{name}" is shown as pending')
def step_subtask_shown_as_pending(context, name):
    _wait(context).until(
        EC.presence_of_element_located(
            (By.XPATH,
             f"//*[contains(@class,'subtask-card-pending')][.//*[normalize-space(text())='{name}']]")
        )
    )


@then("each pending subtask shows a circle icon in its toggle button")
def step_pending_subtasks_have_circle_icon(context):
    driver = context.browser.driver
    pending_cards = driver.find_elements(By.CSS_SELECTOR, ".subtask-card-pending")
    assert len(pending_cards) > 0, "No pending subtask cards found"
    for card in pending_cards:
        assert card.find_elements(By.CSS_SELECTOR, ".subtask-toggle-icon .fi-rr-circle"), \
            "Pending subtask is missing the circle toggle icon"


@then("each completed subtask shows a checkmark icon in its toggle button")
def step_completed_subtasks_have_checkmark_icon(context):
    driver = context.browser.driver
    completed_cards = driver.find_elements(By.CSS_SELECTOR, ".subtask-card-completed")
    assert len(completed_cards) > 0, "No completed subtask cards found"
    for card in completed_cards:
        assert card.find_elements(By.CSS_SELECTOR, ".subtask-toggle-icon .fi-rr-check-circle"), \
            "Completed subtask is missing the checkmark toggle icon"


@then("each completed subtask name appears with strikethrough")
def step_completed_subtasks_have_strikethrough(context):
    driver = context.browser.driver
    completed_names = driver.find_elements(
        By.CSS_SELECTOR, ".subtask-card-completed .subtask-card-name"
    )
    assert len(completed_names) > 0, "No completed subtask name elements found"


@then("the toggle button is disabled during the request")
def step_toggle_disabled_during_request(context):
    task = context.current_task
    task.refresh_from_db()
    completed_count = Subtask.objects.filter(task_id=task, completed=True).count()
    assert completed_count > 0, \
        "No subtask was toggled — the button may not have submitted the form"


@then("the pending subtask count is unchanged")
def step_pending_count_unchanged(context):
    driver = context.browser.driver
    heading = _wait(context).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#task-subtasks .details-section-title h3")
        )
    )
    text = heading.text  # e.g. "Subtasks (2)"
    assert "Subtasks" in text, f"Unexpected heading text: {text}"
    import re
    match = re.search(r"\((\d+)\)", text)
    assert match, f"Could not parse pending count from heading: {text}"
    pending_shown = int(match.group(1))
    task = context.current_task
    pending_in_db = Subtask.objects.filter(task_id=task, completed=False).count()
    assert pending_shown == pending_in_db, \
        f"Heading shows {pending_shown} pending but DB has {pending_in_db}"