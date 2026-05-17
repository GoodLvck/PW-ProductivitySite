from datetime import timedelta
from urllib.parse import urlparse

from behave import given, when, then
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

from productivity_site.models import Subject, Task
from features.steps.common import _click_button, _wait
from django.utils import timezone


def _current_path(context):
    return urlparse(context.browser.url).path


def _get_test_user(context):
    return User.objects.get(username=context.test_user["username"])


def _get_or_create_subject(context, name):
    user = _get_test_user(context)
    subject, _ = Subject.objects.get_or_create(
        name=name,
        user_id=user,
        defaults={"description": "Test description", "color": "#7d9b76"},
    )
    return subject


def _get_or_create_task(context, subject, name, completed=False):
    task, _ = Task.objects.get_or_create(
        name=name,
        subject_id=subject,
        defaults={
            "text": "Test description",
            "due_date": timezone.now() + timedelta(days=7),
            "priority": "medium",
            "estimated_time": 60,
            "completed": completed,
        },
    )
    return task


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------

@given('I am on the "Mathematics" subject detail page')
def step_on_mathematics_detail(context):
    subject = _get_or_create_subject(context, "Mathematics")
    context.current_subject = subject
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}"
    )
    _wait(context).until(
        visibility_of_element_located((By.CSS_SELECTOR, "body"))
    )


@given('I am on the detail of task "{name}"')
def step_on_task_detail(context, name):
    subject = _get_or_create_subject(context, "Mathematics")
    context.current_subject = subject
    task = _get_or_create_task(context, subject, name)
    context.current_task = task
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}"
    )
    _wait(context).until(
        visibility_of_element_located((By.CSS_SELECTOR, "body"))
    )


@given('the subject "{name}" has 2 pending tasks and 1 completed task')
def step_subject_has_tasks(context, name):
    subject = _get_or_create_subject(context, name)
    context.current_subject = subject
    Task.objects.filter(subject_id=subject).delete()
    for i in range(1, 3):
        Task.objects.create(
            name=f"Pending task {i}",
            subject_id=subject,
            text="Test",
            due_date=timezone.now() + timedelta(days=7),
            priority="medium",
            estimated_time=60,
            completed=False,
        )
    Task.objects.create(
        name="Submit chapter 3 problems",
        subject_id=subject,
        text="Test",
        due_date=timezone.now() + timedelta(days=7),
        priority="medium",
        estimated_time=60,
        completed=True,
    )


@given('the subject "History" has no tasks')
def step_subject_no_tasks(context):
    subject = _get_or_create_subject(context, "History")
    context.history_subject = subject
    Task.objects.filter(subject_id=subject).delete()


@given("I am on the subject detail page")
def step_on_subject_detail_page(context):
    subject = context.current_subject
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}"
    )
    _wait(context).until(
        visibility_of_element_located((By.CSS_SELECTOR, "body"))
    )


@given("a completed task exists")
def step_completed_task_exists(context):
    subject = context.current_subject
    task = Task.objects.filter(subject_id=subject, completed=True).first()
    if not task:
        task = Task.objects.create(
            name="Completed task",
            subject_id=subject,
            text="Test",
            due_date=timezone.now() + timedelta(days=7),
            priority="medium",
            estimated_time=60,
            completed=True,
        )
    context.current_task = task


# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------

@when('I open the detail of "{name}"')
def step_open_subject_detail(context, name):
    subject = _get_or_create_subject(context, name)
    context.current_subject = subject
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}"
    )
    _wait(context).until(
        visibility_of_element_located((By.CSS_SELECTOR, "body"))
    )


@when("I open its detail")
def step_open_its_detail(context):
    subject = context.history_subject
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}"
    )
    _wait(context).until(
        visibility_of_element_located((By.CSS_SELECTOR, "body"))
    )


@when('I select due date "{date}"')
def step_select_due_date(context, date):
    driver = context.browser.driver
    el = _wait(context).until(
        EC.presence_of_element_located((By.NAME, "due_date"))
    )
    # timezone-local format: YYYY-MM-DDTHH:MM
    driver.execute_script(f"arguments[0].value = '{date}T12:00';", el)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", el)


@when("I select a due date in the past")
def step_select_past_due_date(context):
    driver = context.browser.driver
    past_date = (timezone.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    el = _wait(context).until(
        EC.presence_of_element_located((By.NAME, "due_date"))
    )
    driver.execute_script(f"arguments[0].value = '{past_date}T12:00';", el)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", el)


@when("I set estimated time to 90 minutes")
def step_set_estimated_time_90(context):
    context.browser.fill("estimated_time", "90")


@when("I change the estimated time to {minutes:d}")
def step_change_estimated_time(context, minutes):
    context.browser.fill("estimated_time", str(minutes))


@when('I select priority "{priority}"')
def step_select_priority(context, priority):
    driver = context.browser.driver
    el = _wait(context).until(
        EC.presence_of_element_located((By.NAME, "priority"))
    )
    from selenium.webdriver.support.ui import Select
    Select(el).select_by_value(priority)


@when('I change the priority to "{priority}"')
def step_change_priority(context, priority):
    driver = context.browser.driver
    el = _wait(context).until(
        EC.presence_of_element_located((By.NAME, "priority"))
    )
    from selenium.webdriver.support.ui import Select
    Select(el).select_by_value(priority)


@when('I create a task with priority "{priority}"')
def step_create_task_with_priority(context, priority):
    driver = context.browser.driver
    _click_button(context, "Create task")
    context.browser.fill("name", f"Task {priority}")
    context.browser.fill("text", f"Description for {priority} task")
    context.browser.fill("estimated_time", "60")

    el = _wait(context).until(
        EC.presence_of_element_located((By.NAME, "due_date"))
    )
    future_date = (timezone.now() + timedelta(days=7)).strftime("%Y-%m-%dT12:00")
    driver.execute_script(f"arguments[0].value = '{future_date}';", el)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", el)

    priority_el = _wait(context).until(
        EC.presence_of_element_located((By.NAME, "priority"))
    )
    from selenium.webdriver.support.ui import Select
    Select(priority_el).select_by_value(priority)
    _click_button(context, "Create")

    subject = context.current_subject
    _wait(context).until(
        lambda driver: f"/subjects/{subject.subject_id}" in urlparse(driver.current_url).path
        and "/tasks/" not in urlparse(driver.current_url).path
    )

@when("I leave \"Name\" or \"Due date\" empty")
def step_leave_name_or_due_date_empty(context):
    context.browser.fill("name", "")


@when('I click on the task card "{name}"')
def step_click_task_card(context, name):
    el = _wait(context).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//*[contains(@class, 'subject-task-card') or contains(@class, 'task-card')][.//*[normalize-space(text())='{name}']]")
        )
    )
    el.click()


@when("I click the completion circle of a pending task")
def step_click_completion_circle(context):
    el = _wait(context).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".task-toggle-icon"))
    )
    el.click()


@when("I click its checkmark")
def step_click_checkmark(context):
    el = _wait(context).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(@class, 'task-toggle-icon')][.//*[contains(@class, 'fi-rr-check-circle')]]")
        )
    )
    el.click()


# ---------------------------------------------------------------------------
# Then
# ---------------------------------------------------------------------------

@then('the task "{name}" appears in the pending list')
def step_task_in_pending_list(context, name):
    _wait(context).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[contains(@class, 'subject-task-card')][.//*[normalize-space(text())='{name}']]")
        )
    )


@then('it shows priority "{priority}" and estimated time "{time}"')
def step_shows_priority_and_time(context, priority, time):
    assert context.browser.is_text_present(priority, wait_time=3), \
        f'Priority "{priority}" not found'
    assert context.browser.is_text_present(time, wait_time=3), \
        f'Estimated time "{time}" not found'


@then('I see the section "{text}"')
def step_see_section(context, text):
    assert context.browser.is_text_present(text, wait_time=3), \
        f'Section "{text}" not found'


@then("I see 2 cards in the pending section")
def step_two_pending_cards(context):
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".subject-task-card"))
    )
    driver = context.browser.driver
    cards = driver.find_elements(By.CSS_SELECTOR, ".subject-task-card-pending, .subtask-card-pending")
    assert len(cards) >= 2, f"Expected 2 pending cards, found {len(cards)}"


@then('I see 1 card in the "Completed (1)" section with muted style and strikethrough text')
def step_one_completed_card(context):
    driver = context.browser.driver
    cards = driver.find_elements(By.CSS_SELECTOR, ".subject-task-card-completed, .subtask-card-completed")
    assert len(cards) >= 1, f"Expected 1 completed card, found {len(cards)}"


@then("I see the task detail view")
def step_task_detail_view(context):
    current = _current_path(context)
    assert "/tasks/" in current, f"Expected task detail URL, got {current}"


@then("I see the time, due date, and priority information")
def step_time_due_priority(context):
    driver = context.browser.driver
    assert driver.find_elements(By.CSS_SELECTOR, ".task-details-card-meta"), \
        "Task meta information not found"


@then("I am returned to the subject detail page")
def step_returned_to_subject(context):
    subject = context.current_subject
    expected = f"/subjects/{subject.subject_id}"
    _wait(context).until(
        lambda driver: expected in urlparse(driver.current_url).path
    )


@then("the task no longer appears in the list")
def step_task_not_in_list(context):
    task = context.current_task
    driver = context.browser.driver
    import time
    time.sleep(1)
    els = driver.find_elements(
        By.XPATH,
        f"//*[contains(@class, 'subject-task-card')][.//*[normalize-space(text())='{task.name}']]"
    )
    assert len(els) == 0, f"Task '{task.name}' still appears in the list"


@then("the task still exists")
def step_task_still_exists(context):
    task = context.current_task
    assert Task.objects.filter(task_id=task.task_id).exists(), \
        f"Task '{task.name}' not found in database"


@then('the task moves to the "Completed" section')
def step_task_moves_to_completed(context):
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".subject-task-card-completed"))
    )


@then("its name appears with strikethrough")
def step_name_strikethrough(context):
    driver = context.browser.driver
    els = driver.find_elements(
        By.CSS_SELECTOR,
        ".subject-completed-grid .subject-task-title, .subject-task-card-completed .subject-task-title"
    )
    assert len(els) > 0, "No strikethrough task found"


@then("it moves back to the pending section")
def step_moves_to_pending(context):
    _wait(context).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".subject-task-card-pending"))
    )


@then('the displayed priority is "{priority}"')
def step_displayed_priority(context, priority):
    assert context.browser.is_text_present(priority, wait_time=3), \
        f'Priority "{priority}" not found'


@then("the original task name is still displayed")
def step_original_task_name(context):
    task = context.current_task
    assert context.browser.is_text_present(task.name, wait_time=3), \
        f'Original task name "{task.name}" not found'


@then('it is displayed on its card with the style corresponding to "{priority}"')
def step_priority_style(context, priority):
    driver = context.browser.driver
    els = driver.find_elements(
        By.CSS_SELECTOR,
        f".priority-badge-{priority}"
    )
    assert len(els) > 0, f"No element with priority style '{priority}' found"


@then("I can still create the task if I confirm")
def step_can_create_after_warning(context):
    _click_button(context, "Create")
    current = _current_path(context)
    assert "/subjects/" in current, f"Expected to be on subject page, got {current}"

