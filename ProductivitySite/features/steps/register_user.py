from behave import *

use_step_matcher("parse")


@when('I register as user "{username}" with email "{email}" and password "{password}"')
def step_impl(context, username, email, password):
    context.browser.visit(f"{context.base_url}/accounts/signup/")
    context.browser.fill("first_name", "Test")
    context.browser.fill("last_name", "User")
    context.browser.fill("username", username)
    context.browser.fill("email", email)
    context.browser.fill("password1", password)
    context.browser.fill("password2", password)
    context.browser.find_by_css('button[type="submit"]').first.click()


@then('there is a registered user with username "{username}"')
def step_impl(context, username):
    from django.contrib.auth.models import User
    assert User.objects.filter(username=username).exists(), \
        f"No user found with username '{username}'"


@then('there is {count:d} user with username "{username}"')
def step_impl(context, count, username):
    from django.contrib.auth.models import User
    actual = User.objects.filter(username=username).count()
    assert actual == count, \
        f"Expected {count} user(s) with username '{username}', found {actual}"


@then("I am on the login page")
def step_impl(context):
    assert "/accounts/login/" in context.browser.url, \
        f"Expected login URL, got {context.browser.url}"
