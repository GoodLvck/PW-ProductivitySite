Feature: Create subtask
  As an authenticated user
  I want to break a task down into subtasks
  So that I can manage it more easily

  Background:
    Given I am logged in
    And I am on the detail of task "Submit chapter 3 problems"

  Scenario: Create a subtask manually
    When I click "New subtask"
    And I fill in "Name" with "Solve exercise 1"
    And I set estimated time to 30
    And I select priority "medium"
    And I click "Create"
    Then the subtask "Solve exercise 1" appears in the list
    And the subtask counter increases by 1

  Scenario: Generate subtasks with AI
    Given the task has no subtasks yet
    When I click "Generate with AI"
    And I confirm the generation
    Then several suggested subtasks are added to the list

  Scenario: AI generation is disabled when subtasks already exist
    Given the task already has at least one subtask
    Then the "Generate with AI" button is disabled

  Scenario: Required name validation
    When I click "New subtask"
    And I leave "Name" empty
    Then the "Create" button remains disabled
