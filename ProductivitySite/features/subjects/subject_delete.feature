@wip
Feature: Delete subject
  As an authenticated user
  I want to delete a subject
  So that I can keep my list clean

  Background:
    Given I am logged in
    And I am on the detail page of subject "History"

  Scenario: Confirmed deletion
    When I click the floating "Edit" button
    And I click "Delete"
    And I confirm the deletion
    Then I am returned to "/subjects"
    And the subject "History" no longer appears in the grid

  Scenario: Cancel deletion
    When I click the floating "Edit" button
    And I click "Delete"
    And I cancel the confirmation
    Then the subject "History" still exists

  Scenario: Deletion warning when subject has tasks
    Given the subject "History" has 2 tasks
    When I click the floating "Edit" button
    And I click "Delete"
    Then I see a warning "Deleting this subject will also delete its tasks"
    And I must confirm before the deletion proceeds