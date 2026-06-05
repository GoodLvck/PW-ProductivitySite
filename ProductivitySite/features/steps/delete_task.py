from behave import *

use_step_matcher("parse")


@when('I delete task "{task_name}" in subject "{subject_name}"')
def step_impl(context, task_name, subject_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject, Task

    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)
    task = Task.objects.get(subject_id=subject, name=task_name)

    # 1. Navigate to the task detail page (which renders the floating actions)
    context.browser.visit(
        f"{context.base_url}/subjects/{subject.subject_id}/tasks/{task.task_id}"
    )

    # 2. Open the floating actions menu
    context.browser.find_by_css(".floating-actions-toggle").first.click()

    # 3. Click the Delete button to open the confirmation popover
    context.browser.find_by_css(".floating-actions-delete").first.click()

    # 4. Confirm deletion
    context.browser.find_by_css(".button-destructive").first.click()
