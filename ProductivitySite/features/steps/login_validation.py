from behave import *

use_step_matcher("parse")


@when('I try to login as "{username}" with password "{password}"')
def step_impl(context, username, password):
    context.browser.visit(f"{context.base_url}/accounts/login/")
    context.browser.fill("username", username)
    context.browser.fill("password", password)
    context.browser.find_by_css('button[type="submit"]').first.click()


@then("I remain on the login page")
def step_impl(context):
    assert "/accounts/login/" in context.browser.url, \
        f"Expected to remain on the login page, got {context.browser.url}"
