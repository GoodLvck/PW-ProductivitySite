from behave import *

use_step_matcher("parse")


@when('I visit the details page for task "{task_name}" in subject "{subject_name}"')
def step_impl(context, task_name, subject_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject, Task
    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)
    task = Task.objects.get(subject_id=subject, name=task_name)
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}"
    )


@then('I can see the task name "{name}"')
def step_impl(context, name):
    assert context.browser.is_text_present(name), \
        f"Task name '{name}' not found on the page"


@then("there are no subtasks listed")
def step_impl(context):
    assert context.browser.is_text_present("There are no subtasks. Create the first one!"), \
        "Expected empty-subtask message not found on page"


@then('I can see the subtask "{name}"')
def step_impl(context, name):
    assert context.browser.is_text_present(name), \
        f"Subtask '{name}' not found on the task page"
