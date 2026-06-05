Feature: Create Subtask
  In order to break down my tasks into smaller steps
  As a registered user
  I want to create a subtask within a task

  Background: There is a registered user with a task
    Given I am logged in as "testuser" with password "TestPass123!"
    And there is a subject named "Mathematics"
    And there is a task "Algebra exam" in subject "Mathematics" due "2027-12-31T23:59" taking 120 minutes

  Scenario: Create a subtask with required fields
    When I create a subtask in task "Algebra exam" of subject "Mathematics" with:
      | name         | description         | due_date         | priority | estimated_time |
      | Review notes | Go over class notes | 2027-12-30T23:59 | medium   | 45             |
    Then I am viewing the task "Algebra exam" in subject "Mathematics"
    And there is 1 subtask named "Review notes" in task "Algebra exam"

  Scenario: Cannot create two subtasks with the same name in the same task
    Given there is a subtask "Review notes" in task "Algebra exam" of subject "Mathematics" due "2027-12-30T23:59" taking 30 minutes
    When I create a subtask in task "Algebra exam" of subject "Mathematics" with:
      | name         | description    | due_date         | priority | estimated_time |
      | Review notes | Another notes  | 2027-12-30T23:59 | low      | 20             |
    Then I see an error message "A subtask with that name already exists"

  Scenario: Cannot create a subtask with a due date in the past
    When I create a subtask in task "Algebra exam" of subject "Mathematics" with:
      | name       | description | due_date         | priority | estimated_time |
      | Past notes | Old stuff   | 2020-01-01T00:00 | medium   | 30             |
    Then I see an error message "Due date cannot be in the past"

  Scenario: Cannot create a subtask with a due date after the task's due date
    When I create a subtask in task "Algebra exam" of subject "Mathematics" with:
      | name       | description | due_date         | priority | estimated_time |
      | Late notes | Late stuff  | 2028-01-01T00:00 | medium   | 30             |
    Then I see an error message "Subtask due date cannot be after the task due date"

  Scenario: Cannot create a subtask with zero estimated time
    When I create a subtask in task "Algebra exam" of subject "Mathematics" with:
      | name        | description | due_date         | priority | estimated_time |
      | Quick notes | Fast stuff  | 2027-12-30T23:59 | medium   | 0              |
    Then I see an error message "Estimated time must be greater than 0"
