@wip
Feature: View tasks
  As an authenticated user
  I want to see the tasks of a subject and open their detail
  So that I can track my workload

  Background:
    Given I am logged in
    And the subject "Mathematics" has 2 pending tasks and 1 completed task

  Scenario: Task list in the subject detail
    When I open the detail of "Mathematics"
    Then I see the section "Tasks (2)"
    And I see 2 cards in the pending section
    And I see 1 card in the "Completed (1)" section with muted style and strikethrough text

  Scenario: Empty state for tasks
    Given the subject "History" has no tasks
    When I open its detail
    Then I see the message "NO PENDING TASKS!!"

  Scenario: Open task detail
    When I open the detail of "Mathematics"
    And I click on the task card "Submit chapter 3 problems"
    Then I see the task detail view
    And I see the breadcrumb "Subjects / Mathematics / Submit chapter 3 problems"
    And I see the time, due date, and priority information

#  Scenario: Subtask progress on the task card
#    Given the task has 4 subtasks and 2 are completed
#    Then the card shows "2/4" and a progress bar at 50%

#  Scenario: Overdue task is visually highlighted
#    Given a pending task has a due date in the past
#    Then the task card displays a visual overdue indicator
