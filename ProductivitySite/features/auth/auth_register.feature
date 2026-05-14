Feature: User registration
  As a visitor
  I want to create an account on ZenOrbit
  So that I can access the productivity and study features

  Background:
    Given I am on the "/register" page

  Scenario: Successful registration with valid data
    When I fill in "First name" with "Ana"
    And I fill in "Last name" with "Lopez"
    And I fill in "Username" with "newuser2026"
    And I fill in "Email address" with "newuser2026@example.com"
    And I fill in "Password" with "Secret123!"
    And I fill in "Password confirmation" with "Secret123!"
    And I click "Create account"
    Then I am redirected to "/login"

  @wip
  Scenario: Username already taken
    Given a user with username "testuser" already exists
    When I fill in "Username" with "testuser"
    And I fill in "Password" with "Secret123!"
    And I fill in "Password confirmation" with "Secret123!"
    And I click "Create account"
    Then I see the error message "A user with that username already exists."
    And I remain on "/register"

  @wip
  Scenario: Weak password
    When I fill in "Username" with "weakpwduser"
    And I fill in "Password" with "short"
    And I fill in "Password confirmation" with "short"
    And I click "Create account"
    Then I see the error message "This password is too short"

#  Scenario Outline: Required field validation
#    When I leave the "<field>" field empty
#    And I click "Create account"
#    Then I see the message "<message>"
#
#    Examples:
#      | field    | message                |
#      | Username | This field is required |
#      | Password | This field is required |
