@wip
Feature: Edit and complete tasks
  As an authenticated user
  I want to modify tasks and mark them as completed
  So that I can keep my work up to date

  Background:
    Given I am logged in
    And I am on the detail of task "Submit chapter 3 problems"

  Scenario: Edit task fields
    When I click "Edit"
    And I change the name to "Submit chapter 3 and 4 problems"
    And I change the estimated time to 120
    And I change the priority to "medium"
    And I click "Save"
    Then the title shows "Submit chapter 3 and 4 problems"
    And the displayed priority is "medium"

  Scenario: Mark task as completed from the list
    Given I am on the subject detail page
    When I click the completion circle of a pending task
    Then the task moves to the "Completed" section
    And its name appears with strikethrough

  Scenario: Unmark a completed task
    Given a completed task exists
    When I click its checkmark
    Then it moves back to the pending section

  Scenario: Edit is cancelled without saving
    When I click "Edit"
    And I change the name to "Something else"
    And I click "Cancel"
    Then the original task name is still displayed
