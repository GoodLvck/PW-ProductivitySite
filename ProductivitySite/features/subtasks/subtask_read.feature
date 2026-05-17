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

  Scenario: Open subtask detail
    When I open the task detail
    And I click on a subtask
    Then I see the subtask detail view with all its fields

  Scenario: Empty state
    Given the task has no subtasks
    When I open the task detail
    Then I see the message "There are no subtasks. Create the first one!"