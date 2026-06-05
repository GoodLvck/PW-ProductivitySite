from behave import *

use_step_matcher("parse")


@when('I delete subject "{subject_name}"')
def step_impl(context, subject_name):
    from django.contrib.auth.models import User
    from productivity_site.models import Subject

    user = User.objects.get(username=context.test_user["username"])
    subject = Subject.objects.get(user_id=user, name=subject_name)

    # 1. Navigate to the subject detail page (which renders the floating actions)
    context.browser.visit(f"{context.base_url}/subjects/{subject.subject_id}")

    # 2. Open the floating actions menu (pencil toggle button)
    context.browser.find_by_css(".floating-actions-toggle").first.click()

    # 3. Click the Delete button inside the menu to open the confirmation popover
    context.browser.find_by_css(".floating-actions-delete").first.click()

    # 4. Confirm deletion by clicking the destructive submit button in the popover
    context.browser.find_by_css(".button-destructive").first.click()
