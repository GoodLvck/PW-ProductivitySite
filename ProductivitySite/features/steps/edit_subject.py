from behave import *

use_step_matcher("parse")


@when('I edit subject "{subject_name}" with:')
def step_impl(context, subject_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject

    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)
    context.browser.visit(f"{context.base_url}/subjects/{subject.subject_id}/update")

    row = context.table.rows[0]
    for heading in context.table.headings:
        # Clear the existing value and type the new one
        field = context.browser.find_by_css(f'[name="{heading}"]').first
        field._element.clear()
        field._element.send_keys(row[heading])

    context.browser.find_by_css('button[type="submit"]').first.click()


@then('the subject name displayed is "{name}"')
def step_impl(context, name):
    assert context.browser.is_text_present(name), \
        f"Subject name '{name}' not found on the page"
