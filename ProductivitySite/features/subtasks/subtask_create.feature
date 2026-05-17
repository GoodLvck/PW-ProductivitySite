@wip
Feature: Create subtask
  As an authenticated user
  I want to break a task down into subtasks
  So that I can manage it more easily

  Background:
    Given I am logged in
    And I am on the detail of task "Submit chapter 3 problems"

  Scenario: Create a subtask manually
    When I click "Create subtask"
    And I fill in "Name" with "Solve exercise 1"
    And I fill in "Description" with "Test description"
    And I set estimated time to 30
    And I select due date "2026-06-01"
    And I select priority "medium"
    And I click "Create"
    Then the subtask "Solve exercise 1" appears in the list
    And the subtask counter increases by 1

  Scenario: Created subtask appears as pending by default
    When I click "Create subtask"
    And I fill in "Name" with "Solve exercise 2"
    And I fill in "Description" with "Test description"
    And I set estimated time to 15
    And I select due date "2026-06-01"
    And I select priority "low"
    And I click "Create"
    Then the subtask "Solve exercise 2" appears in the list
    And the subtask "Solve exercise 2" is shown as pending

#  Scenario: Generate subtasks with AI
#    Given the task has no subtasks yet
#    When I click "Generate with AI"
#    And I confirm the generation
#    Then several suggested subtasks are added to the list

#  Scenario: AI generation is disabled when subtasks already exist
#    Given the task already has at least one subtask
#    Then the "Generate with AI" button is disabled

  Scenario: Required name validation
    When I click "Create subtask"
    And I leave the "Name" field empty
    And I click "Create"
    Then I see the message "Name is required"
