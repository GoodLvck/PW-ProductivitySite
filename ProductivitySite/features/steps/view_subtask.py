from behave import *

use_step_matcher("parse")


@when('I visit the details page for subtask "{subtask_name}" in task "{task_name}" of subject "{subject_name}"')
def step_impl(context, subtask_name, task_name, subject_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject, Task, Subtask
    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)
    task = Task.objects.get(subject_id=subject, name=task_name)
    subtask = Subtask.objects.get(task_id=task, name=subtask_name)
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}"
        f"/tasks/{task.task_id}/subtasks/{subtask.subtask_id}"
    )


@then('I can see the subtask name "{name}"')
def step_impl(context, name):
    assert context.browser.is_text_present(name), \
        f"Subtask name '{name}' not found on the page"


@then('I can see the task it belongs to "{task_name}"')
def step_impl(context, task_name):
    assert context.browser.is_text_present(task_name), \
        f"Parent task name '{task_name}' not found on the subtask page"


@then('I can see the subject it belongs to "{subject_name}"')
def step_impl(context, subject_name):
    assert context.browser.is_text_present(subject_name), \
        f"Parent subject name '{subject_name}' not found on the subtask page"
