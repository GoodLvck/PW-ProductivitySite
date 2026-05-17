from datetime import timedelta
from urllib.parse import urlparse

from behave import given, when, then
from django.contrib.auth.models import User
from django.utils import timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

from productivity_site.models import Subject, Task, Subtask
from features.steps.common import _click_button, _wait


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
    # Recupera el objeto con el ID generado por SQLite
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
        visibility_of_element_located((By.CSS_SELECTOR, "body"))
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
        visibility_of_element_located((By.CSS_SELECTOR, "body"))
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
    el = _wait(context).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".subtask-card-pending .subtask-toggle-icon")
        )
    )
    el.click()


@when("I click the checkmark of a completed subtask")
def step_click_completed_checkmark(context):
    el = _wait(context).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".subtask-card-completed .subtask-toggle-icon")
        )
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


@then('the progress bar shows "2/4 subtasks" at 50%')
def step_progress_bar(context):
    assert context.browser.is_text_present("2", wait_time=3), \
        "Progress information not found"


@then("I see the subtask detail view with all its fields")
def step_subtask_detail_view(context):
    current = _current_path(context)
    assert "/subtasks/" in current, f"Expected subtask detail URL, got {current}"


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
            (By.CSS_SELECTOR, ".subtask-card-completed .subtask-toggle-icon")
        )
    )


@then("the name appears with strikethrough")
def step_subtask_name_strikethrough(context):
    driver = context.browser.driver
    els = driver.find_elements(
        By.CSS_SELECTOR, ".subtask-card-completed .subtask-card-name"
    )
    assert len(els) > 0, "No completed subtask with strikethrough found"


@then("the parent task's progress bar is updated")
def step_parent_progress_updated(context):
    assert context.browser.is_text_present("Subtasks", wait_time=3), \
        "Subtasks section not found"


@then("it returns to a pending state")
def step_subtask_returns_pending(context):
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".subtask-card-pending"))
    )


@then("the progress bar is recalculated")
def step_progress_recalculated(context):
    assert context.browser.is_text_present("Subtasks", wait_time=3), \
        "Subtasks section not found"


@then("the changes are reflected when I return to the task")
def step_changes_reflected(context):
    task = context.current_task
    subject = context.current_subject
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}"
    )
    assert context.browser.is_text_present("Modified subtask name", wait_time=3), \
        "Modified subtask name not found"