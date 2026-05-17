@wip
Feature: Edit and complete subtasks
  As an authenticated user
  I want to modify subtasks and mark them as done
  So that I can keep track of granular progress

  Background:
    Given I am logged in
    And I am on the detail of a task with several subtasks

  Scenario: Mark subtask as done from the task detail list
    When I click the circle of a pending subtask
    Then the icon changes to a completed checkmark
    And the name appears with strikethrough
    And the parent task's progress bar is updated

  Scenario: Unmark a completed subtask from the task detail list
    When I click the checkmark of a completed subtask
    Then it returns to a pending state
    And the progress bar is recalculated

  Scenario: Toggle is disabled while the request is in flight
    When I click the circle of a pending subtask
    Then the toggle button is disabled during the request

  Scenario: Mark subtask as done from the subtask detail page
    Given I am on the subtask detail page of a pending subtask
    When I click the status card to toggle completion
    Then the status card shows completed

  Scenario: Unmark a subtask from the subtask detail page
    Given I am on the subtask detail page of a completed subtask
    When I click the status card to toggle completion
    Then the status card shows pending

  Scenario: Toggling from the detail page is reflected in the task list
    Given I am logged in
     And I am on the detail of a task with several subtasks
     Given I am on the subtask detail page of a pending subtask
     When I click the status card to toggle completion
     And I navigate back to the task detail page
     Then the parent task's progress bar is updated

  Scenario: Edit subtask
    Given I am on the subtask detail page
    When I click "Edit"
    And I modify the name, description, time, or priority
    And I click "Save"
    Then the changes are reflected when I return to the task