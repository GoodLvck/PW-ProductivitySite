from behave import *

use_step_matcher("parse")


@when('I visit the details page for subject "{name}"')
def step_impl(context, name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject
    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=name)
    context.browser.visit(f"{context.base_url}/subjects/{subject.subject_id}")


@then('I can see the subject name "{name}"')
def step_impl(context, name):
    assert context.browser.is_text_present(name), \
        f"Subject name '{name}' not found on the page"


@then("there are no tasks listed")
def step_impl(context):
    assert context.browser.is_text_present("NO PENDING TASKS!!"), \
        "Expected empty-task message 'NO PENDING TASKS!!' not found on page"


@then('I can see the task "{name}"')
def step_impl(context, name):
    assert context.browser.is_text_present(name), \
        f"Task '{name}' not found on the subject page"
