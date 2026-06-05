from behave import *

use_step_matcher("parse")


@given('I am logged in as "{username}" with password "{password}"')
def step_impl(context, username, password):
    # Log out any active session first so the login page is always reachable
    context.browser.visit(f"{context.base_url}/logout/")
    context.browser.visit(f"{context.base_url}/accounts/login/")
    context.browser.fill("username", username)
    context.browser.fill("password", password)
    context.browser.find_by_css('button[type="submit"]').first.click()


@given('exists a user "{username}" with password "{password}"')
def step_impl(context, username, password):
    from django.contrib.auth.models import User
    user, _ = User.objects.get_or_create(
        username=username,
        defaults={"email": f"{username}@example.com"},
    )
    user.set_password(password)
    user.save()
