@wip
Feature: Create task
  As an authenticated user
  I want to create tasks within a subject
  So that I can plan my work

  Background:
    Given I am logged in
    And I am on the "Mathematics" subject detail page

  Scenario: Create a task with valid data
    When I click "New task"
    And I fill in "Name" with "Submit chapter 3 problems"
    And I fill in "Description" with "Exercises 1 to 10"
    And I select due date "2026-06-01"
    And I set estimated time to 90 minutes
    And I select priority "high"
    And I click "Create"
    Then the task "Submit chapter 3 problems" appears in the pending list
    And it shows priority "high" and estimated time "90 min"

  Scenario: Missing required fields
    When I click "New task"
    And I leave "Name" or "Due date" empty
    Then the "Create" button remains disabled

  Scenario: Due date in the past
    When I click "New task"
    And I select a due date in the past
    Then I see a warning "The due date is in the past"
    And I can still create the task if I confirm

  Scenario Outline: Create tasks with different priorities
    When I create a task with priority "<priority>"
    Then it is displayed on its card with the style corresponding to "<priority>"

    Examples:
      | priority |
      | high     |
      | medium   |
      | low      |
