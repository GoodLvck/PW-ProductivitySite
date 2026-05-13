Feature: Login
  As a registered user
  I want to log in
  So that I can access my personal workspace

  Background:
    Given I am on the "/login" page

  Scenario: Successful login
    When I enter "ana@example.com" in "Email"
    And I enter "Secret123" in "Password"
    And I click "Sign in"
    Then I am redirected to "/dashboard"
    And I see the sidebar with my session active

  Scenario: Invalid credentials
    When I enter an invalid email or password
    And I click "Sign in"
    Then I see the message "Invalid credentials"
    And I remain on "/login"

  Scenario: Rate limiting after repeated failures
    When I submit incorrect credentials 5 times in a row
    Then I see the message "Too many attempts. Please try again later"
    And the "Sign in" button is disabled temporarily

  Scenario: Access the password recovery page
    When I click the "Forgot your password?" link
    Then I am redirected to "/recover-password"
