Feature: Logout
  As an authenticated user
  I want to log out
  So that I can protect access to my account

  Scenario: Logout from the user menu
    Given I am logged in
    And I am on "/dashboard"
    When I open the user menu in the header
    And I click "Log out"
    Then my session is closed
    And I am redirected to "/login"

  Scenario: Session expires after inactivity
    Given I am logged in
    When my session has been inactive for the configured timeout period
    Then I am automatically logged out
    And I am redirected to "/login"
    And I see the message "Your session has expired. Please log in again"
