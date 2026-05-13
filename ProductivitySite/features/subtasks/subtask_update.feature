Feature: Edit and complete subtasks
  As an authenticated user
  I want to modify subtasks and mark them as done
  So that I can keep track of granular progress

  Background:
    Given I am logged in
    And I am on the detail of a task with several subtasks

  Scenario: Mark subtask as done
    When I click the circle of a pending subtask
    Then the icon changes to a completed checkmark
    And the name appears with strikethrough
    And the parent task's progress bar is updated

  Scenario: Unmark a completed subtask
    When I click the checkmark of a completed subtask
    Then it returns to a pending state
    And the progress bar is recalculated

  Scenario: Edit subtask
    Given I am on the subtask detail page
    When I click "Edit"
    And I modify the name, description, time, or priority
    And I click "Save"
    Then the changes are reflected when I return to the task
