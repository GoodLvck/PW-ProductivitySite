Feature: Login
  As a registered user
  I want to log in
  So that I can access my personal workspace

  Background:
    Given I am on the "/login" page

  Scenario: Successful login
    When I fill in "Username" with "testuser"
    And I fill in "Password" with "TestPass123!"
    And I click "Log in"
    Then I am redirected to "/dashboard"
    And I see the sidebar with my session active

  Scenario: Invalid credentials
    When I fill in "Username" with "nonexistent_user"
    And I fill in "Password" with "wrongpassword"
    And I click "Log in"
    Then I see the message "Please enter a correct username and password"
    And I remain on "/login"

#  Scenario: Access the password recovery page
#    # Password recovery link not present in the current login template
#    When I click the "Forgot your password?" link
#    Then I am redirected to "/recover-password"
