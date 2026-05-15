Feature: Logout
  As an authenticated user
  I want to log out
  So that I can protect access to my account

  Scenario: Logout from the sidebar
    Given I am logged in
    And I am on any page within the DashboardLayout
    When I click "Log out"
    Then my session is closed
    And I am redirected to "/"
