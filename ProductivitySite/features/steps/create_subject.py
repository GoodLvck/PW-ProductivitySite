from behave import *

use_step_matcher("parse")


# ---------------------------------------------------------------------------
# Shared Given steps (reused by other features via their Background)
# ---------------------------------------------------------------------------

@given('there is a subject named "{name}"')
def step_impl(context, name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject
    user = User.objects.get(username=context.test_user["username"])
    Subject.objects.get_or_create(
        user_id=user,
        name=name,
        defaults={"description": f"Description for {name}"},
    )


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------

@when("I create a subject with:")
def step_impl(context):
    context.browser.visit(f"{context.base_url}/subjects/create")
    row = context.table.rows[0]
    for heading in context.table.headings:
        context.browser.fill(heading, row[heading])
    context.browser.find_by_css('button[type="submit"]').first.click()


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------

@then("I am on the subjects page")
def step_impl(context):
    assert context.browser.url.rstrip("/").endswith("/subjects"), \
        f"Expected subjects page URL, got {context.browser.url}"


@then('there is {count:d} subject named "{name}"')
def step_impl(context, count, name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject
    user = User.objects.get(username=context.test_user["username"])
    actual = Subject.objects.filter(user_id=user, name=name).count()
    assert actual == count, \
        f"Expected {count} subject(s) named '{name}', found {actual}"


@then('there are {count:d} subjects for the current user')
def step_impl(context, count):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject
    user = User.objects.get(username=context.test_user["username"])
    actual = Subject.objects.filter(user_id=user).count()
    assert actual == count, \
        f"Expected {count} subject(s) for current user, found {actual}"


@then('I see an error message "{message}"')
def step_impl(context, message):
    assert context.browser.is_text_present(message), \
        f"Error message '{message}' not found on page"
