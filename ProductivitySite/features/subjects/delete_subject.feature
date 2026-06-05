Feature: Delete Subject
  In order to remove subjects I no longer need
  As a registered user
  I want to delete a subject

  Background: There is a registered user with a subject
    Given I am logged in as "testuser" with password "TestPass123!"
    And there is a subject named "Mathematics"

  Scenario: Delete a subject
    When I delete subject "Mathematics"
    Then I am on the subjects page
    And there are 0 subjects for the current user
