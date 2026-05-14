Feature: User profile
  As an authenticated user
  I want to view and edit my account data
  So that I can keep my profile up to date

  Background:
    Given I am logged in

  Scenario: View profile
    When I navigate to "/profile"
    Then I see my name, email, and current plan

  @wip
  Scenario: Edit profile data
    When I navigate to "/profile"
    And I modify my name
    And I save the changes
    Then the name is updated in the profile and in the header

  @wip
  Scenario: Change password from profile
    When I navigate to "/profile"
    And I click "Change password"
    And I enter my current password and a new password
    And I click "Save"
    Then I see the message "Password updated successfully"

  @wip
  Scenario: Invalid current password when changing password
    When I navigate to "/profile"
    And I enter an incorrect current password
    And I click "Save"
    Then I see the error message "Current password is incorrect"
