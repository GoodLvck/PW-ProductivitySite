@wip
Feature: Delete task
  As an authenticated user
  I want to delete a task
  So that I can discard work that is no longer relevant

  Background:
    Given I am logged in
    And I am on the detail of task "Submit chapter 3 problems"

  Scenario: Confirmed deletion
    When I click the floating "Edit" button
    And I click "Delete"
    And I confirm the deletion
    Then I am returned to the subject detail page
    And the task no longer appears in the list

  Scenario: Cancel deletion
    When I click the floating "Edit" button
    And I click "Delete"
    And I cancel the confirmation
    Then the task still exists
