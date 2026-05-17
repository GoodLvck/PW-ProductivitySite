Feature: Login
  As a registered user
  I want to log in
  So that I can access my personal workspace

  Background:
    Given I am on the "/login" page

  Scenario: Successful login
    When I enter "testuser" in "Username"
    And I enter "TestPass123!" in "Password"
    And I click "Log in"
    Then I am redirected to "/dashboard"
    And I see the sidebar with my session active

  Scenario: Invalid credentials
    When I enter an invalid username or password
    And I click "Log in"
    Then I see the message "Invalid credentials"
    And I remain on "/login"
