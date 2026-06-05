from behave import *

use_step_matcher("parse")


# ---------------------------------------------------------------------------
# Shared Given steps (reused by view_task feature)
# ---------------------------------------------------------------------------

@given('there is a subtask "{name}" in task "{task_name}" of subject "{subject_name}" due "{due_date}" taking {minutes:d} minutes')
def step_impl(context, name, task_name, subject_name, due_date, minutes):
    from datetime import datetime
    from django.contrib.auth.models import User
    from django.utils import timezone
    from productivity_site.models import Subject, Task, Subtask

    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)
    task = Task.objects.get(subject_id=subject, name=task_name)

    dt = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")
    due_date_aware = timezone.make_aware(dt)

    Subtask.objects.get_or_create(
        task_id=task,
        name=name,
        defaults={
            "description": f"Description for {name}",
            "due_date": due_date_aware,
            "priority": "medium",
            "estimated_time": minutes,
        },
    )


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------

def _fill_subtask_form(context, row):
    """Fill all subtask form fields, bypassing HTML5 constraints where needed."""
    for heading in context.table.headings:
        value = row[heading]
        if heading == "due_date":
            context.browser.execute_script(
                f"document.querySelector('[name=\"due_date\"]').value = '{value}';"
            )
        elif heading == "priority":
            context.browser.select("priority", value)
        elif heading == "estimated_time":
            context.browser.execute_script(
                f"var el = document.querySelector('[name=\"estimated_time\"]');"
                f"el.removeAttribute('min');"
                f"el.value = '{value}';"
            )
        else:
            context.browser.fill(heading, value)


@when('I create a subtask in task "{task_name}" of subject "{subject_name}" with:')
def step_impl(context, task_name, subject_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject, Task

    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)
    task = Task.objects.get(subject_id=subject, name=task_name)
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}/subtasks/create"
    )
    _fill_subtask_form(context, context.table.rows[0])
    context.browser.find_by_css('button[type="submit"]').first.click()


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------

@then('I am viewing the task "{task_name}" in subject "{subject_name}"')
def step_impl(context, task_name, subject_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject, Task
    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)
    task = Task.objects.get(subject_id=subject, name=task_name)
    expected = f"/subjects/{subject.subject_id}/tasks/{task.task_id}"
    assert expected in context.browser.url, \
        f"Expected URL with '{expected}', got {context.browser.url}"


@then('there is {count:d} subtask named "{name}" in task "{task_name}"')
def step_impl(context, count, name, task_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Task, Subtask
    user = User.objects.get(username=context.test_user["username"])
    task = Task.objects.get(subject_id__user_id=user, name=task_name)
    actual = Subtask.objects.filter(task_id=task, name=name).count()
    assert actual == count, \
        f"Expected {count} subtask(s) named '{name}' in task '{task_name}', found {actual}"


@then('there are no subtasks named "{name}" in task "{task_name}"')
def step_impl(context, name, task_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Task, Subtask
    user = User.objects.get(username=context.test_user["username"])
    task = Task.objects.get(subject_id__user_id=user, name=task_name)
    count = Subtask.objects.filter(task_id=task, name=name).count()
    assert count == 0, \
        f"Expected no subtask named '{name}' in task '{task_name}', but found {count}"
