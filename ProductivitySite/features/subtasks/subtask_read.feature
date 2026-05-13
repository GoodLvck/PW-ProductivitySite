Feature: View subtasks
  As an authenticated user
  I want to see subtasks and their progress
  So that I can track the breakdown of a task

  Background:
    Given I am logged in
    And the task "Submit chapter 3 problems" has 4 subtasks, 2 completed

  Scenario: Subtask list in the task detail
    When I open the task detail
    Then I see "Subtasks (4)"
    And I see each subtask with its status, name, time, and priority
    And the progress bar shows "2/4 subtasks" at 50%

  Scenario: Open subtask detail
    When I click on a subtask
    Then I see the subtask detail view with all its fields

  Scenario: Empty state
    Given the task has no subtasks
    Then I see the message "No subtasks yet. Create your first one!"
