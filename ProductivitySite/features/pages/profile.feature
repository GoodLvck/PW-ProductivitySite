Feature: User profile
  As an authenticated user
  I want to view and edit my account data
  So that I can keep my profile up to date

  Background:
    Given I am logged in

  Scenario: View profile
    When I navigate to "/profile"
    Then I see my name, email, and current plan

  Scenario: Edit profile data
    When I modify my name
    And I save the changes
    Then the name is updated in the profile and in the header

  Scenario: Change password from profile
    When I navigate to "/profile"
    And I click "Change password"
    And I enter my current password and a new password
    And I click "Save"
    Then I see the message "Password updated successfully"

  Scenario: Invalid current password when changing password
    When I enter an incorrect current password
    And I click "Save"
    Then I see the error "Current password is incorrect"
