@wip
Feature: View subtasks
  As an authenticated user
  I want to see subtasks and their progress
  So that I can track the breakdown of a task

  Background:
    Given I am logged in
    And the task "Submit chapter 3 problems" has 4 subtasks, 2 completed

  Scenario: Subtask list in the task detail
    When I open the task detail
    Then I see "Subtasks (2)"
    And I see each subtask with its status, name, time, and priority

  Scenario: Pending subtasks show a circle toggle icon
    When I open the task detail
    Then each pending subtask shows a circle icon in its toggle button

  Scenario: Completed subtasks show a checkmark toggle icon and strikethrough name
    When I open the task detail
    Then each completed subtask shows a checkmark icon in its toggle button
    And each completed subtask name appears with strikethrough

  Scenario: Open subtask detail
    When I open the task detail
    And I click on a subtask
    Then I see the subtask detail view with all its fields

  Scenario: Subtask detail shows correct toggle status for a pending subtask
    When I open the task detail
    And I click on a pending subtask
    Then I see the subtask detail view with all its fields
    And the status card shows pending

  Scenario: Subtask detail shows correct toggle status for a completed subtask
    When I open the task detail
    And I click on a completed subtask
    Then I see the subtask detail view with all its fields
    And the status card shows completed

  Scenario: Empty state
    Given the task has no subtasks
    When I open the task detail
    Then I see the message "There are no subtasks. Create the first one!"