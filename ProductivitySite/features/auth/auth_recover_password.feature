#Feature: Password recovery
#  As a user who forgot their password
#  I want to request a recovery link
#  So that I can regain access to my account
#
#  Background:
#    Given I am on "/recover-password"
#
#  Scenario: Recovery request with a registered email
#    When I fill in "Email address" with "test@example.com"
#    And I click "Send link"
#    Then I see the message "We have sent you a recovery link"
#
#  Scenario: Unregistered email
#    When I fill in "Email address" with "nobody@example.com"
#    And I click "Send link"
#    Then I see the message "No account found with that email"
#
#  Scenario: Recovery link expires
#    Given a recovery link was sent to "test@example.com"
#    When I try to use the link after it has expired
#    Then I see the message "This link has expired. Please request a new one"
#    And I am redirected to "/recover-password"
