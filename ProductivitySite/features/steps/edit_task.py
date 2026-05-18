from behave import *

use_step_matcher("parse")


@when('I edit task "{task_name}" in subject "{subject_name}" with:')
def step_impl(context, task_name, subject_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject, Task

    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)
    task = Task.objects.get(subject_id=subject, name=task_name)
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}/update"
    )

    row = context.table.rows[0]
    for heading in context.table.headings:
        if heading == "due_date":
            context.browser.execute_script(
                f"document.querySelector('[name=\"due_date\"]').value = '{row[heading]}';"
            )
        elif heading == "priority":
            context.browser.select("priority", row[heading])
        elif heading == "estimated_time":
            context.browser.execute_script(
                f"var el = document.querySelector('[name=\"estimated_time\"]');"
                f"el.removeAttribute('min');"
                f"el.value = '{row[heading]}';"
            )
        else:
            field = context.browser.find_by_css(f'[name="{heading}"]').first
            field._element.clear()
            field._element.send_keys(row[heading])

    context.browser.find_by_css('button[type="submit"]').first.click()


@then('the task name displayed is "{name}"')
def step_impl(context, name):
    assert context.browser.is_text_present(name), \
        f"Task name '{name}' not found on the page"
