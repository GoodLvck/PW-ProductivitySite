from behave import *

use_step_matcher("parse")


@when('I try to access the subject "{name}" of "{owner}"')
def step_impl(context, name, owner):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject
    owner_user = User.objects.get(username=owner)
    subject = Subject.objects.get(user_id=owner_user, name=name)
    context.browser.visit(f"{context.base_url}/subjects/{subject.subject_id}")


@when('I try to access the task "{task_name}" in subject "{subject_name}" of "{owner}"')
def step_impl(context, task_name, subject_name, owner):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject, Task
    owner_user = User.objects.get(username=owner)
    subject = Subject.objects.get(user_id=owner_user, name=subject_name)
    task = Task.objects.get(subject_id=subject, name=task_name)
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}"
    )


@when('I try to access the subtask "{subtask_name}" in task "{task_name}" in subject "{subject_name}" of "{owner}"')
def step_impl(context, subtask_name, task_name, subject_name, owner):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject, Task, Subtask
    owner_user = User.objects.get(username=owner)
    subject = Subject.objects.get(user_id=owner_user, name=subject_name)
    task = Task.objects.get(subject_id=subject, name=task_name)
    subtask = Subtask.objects.get(task_id=task, name=subtask_name)
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}"
        f"/tasks/{task.task_id}/subtasks/{subtask.subtask_id}"
    )


@then("I see a not found page")
def step_impl(context):
    # Django returns HTTP 404 for unauthorized resource access.
    # In DEBUG mode the default page contains "Page not found (404)".
    page_html = context.browser.html
    assert (
        "Page not found" in page_html
        or "404" in page_html
        or "Not Found" in page_html
    ), f"Expected a 404 Not Found page at {context.browser.url}"
