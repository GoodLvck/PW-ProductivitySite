Feature: Create Task
  In order to keep track of my work
  As a registered user
  I want to create a task in a subject

  Background: There is a registered user with a subject
    Given I am logged in as "testuser" with password "TestPass123!"
    And there is a subject named "Mathematics"

  Scenario: Create a task with required fields
    When I create a task in subject "Mathematics" with:
      | name         | text              | due_date         | priority | estimated_time |
      | Algebra exam | Study for algebra | 2027-12-31T23:59 | high     | 120            |
    Then I am viewing the subject "Mathematics"
    And there is 1 task named "Algebra exam" in subject "Mathematics"

  Scenario: Cannot create two tasks with the same name in the same subject
    Given there is a task "Algebra exam" in subject "Mathematics" due "2027-12-31T23:59" taking 60 minutes
    When I create a task in subject "Mathematics" with:
      | name         | text              | due_date         | priority | estimated_time |
      | Algebra exam | Another algebra   | 2027-12-31T23:59 | medium   | 60             |
    Then I see an error message "A task with that name already exists"

  Scenario: Cannot create a task with a due date in the past
    When I create a task in subject "Mathematics" with:
      | name      | text       | due_date         | priority | estimated_time |
      | Past task | Old stuff  | 2020-01-01T00:00 | medium   | 60             |
    Then I see an error message "Due date cannot be in the past"

  Scenario: Cannot create a task with zero estimated time
    When I create a task in subject "Mathematics" with:
      | name       | text        | due_date         | priority | estimated_time |
      | Quick task | Fast stuff  | 2027-12-31T23:59 | medium   | 0              |
    Then I see an error message "Estimated time must be greater than 0"
