from behave import *

use_step_matcher("parse")


# ---------------------------------------------------------------------------
# Shared Given steps (reused by view_task and create_subtask features)
# ---------------------------------------------------------------------------

@given('there is a task "{name}" in subject "{subject_name}" due "{due_date}" taking {minutes:d} minutes')
def step_impl(context, name, subject_name, due_date, minutes):
    from datetime import datetime
    from django.contrib.auth.models import User
    from django.utils import timezone
    from productivity_site.models import Subject, Task

    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)

    dt = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")
    due_date_aware = timezone.make_aware(dt)

    Task.objects.get_or_create(
        subject_id=subject,
        name=name,
        defaults={
            "text": f"Description for {name}",
            "due_date": due_date_aware,
            "priority": "medium",
            "estimated_time": minutes,
        },
    )


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------

def _fill_task_form(context, row):
    """Fill all task form fields, bypassing HTML5 constraints where needed."""
    for heading in context.table.headings:
        value = row[heading]
        if heading == "due_date":
            # Use JS to set datetime-local values reliably
            context.browser.execute_script(
                f"document.querySelector('[name=\"due_date\"]').value = '{value}';"
            )
        elif heading == "priority":
            context.browser.select("priority", value)
        elif heading == "estimated_time":
            # Remove the min="1" HTML attribute so we can test server-side validation
            context.browser.execute_script(
                f"var el = document.querySelector('[name=\"estimated_time\"]');"
                f"el.removeAttribute('min');"
                f"el.value = '{value}';"
            )
        else:
            context.browser.fill(heading, value)


@when('I create a task in subject "{subject_name}" with:')
def step_impl(context, subject_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject

    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}/tasks/create"
    )
    _fill_task_form(context, context.table.rows[0])
    context.browser.find_by_css('button[type="submit"]').first.click()


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------

@then('I am viewing the subject "{subject_name}"')
def step_impl(context, subject_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject
    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)
    assert f"/subjects/{subject.subject_id}" in context.browser.url, \
        f"Expected URL with '/subjects/{subject.subject_id}', got {context.browser.url}"


@then('there is {count:d} task named "{name}" in subject "{subject_name}"')
def step_impl(context, count, name, subject_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject, Task
    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)
    actual = Task.objects.filter(subject_id=subject, name=name).count()
    assert actual == count, \
        f"Expected {count} task(s) named '{name}' in '{subject_name}', found {actual}"


@then('there are no tasks named "{name}" in subject "{subject_name}"')
def step_impl(context, name, subject_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject, Task
    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)
    count = Task.objects.filter(subject_id=subject, name=name).count()
    assert count == 0, \
        f"Expected no task named '{name}' in '{subject_name}', but found {count}"
