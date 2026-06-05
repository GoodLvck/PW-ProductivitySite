Feature: Edit Task
  In order to keep my task information up to date
  As a registered user
  I want to edit an existing task

  Background: There is a registered user with a task
    Given I am logged in as "testuser" with password "TestPass123!"
    And there is a subject named "Mathematics"
    And there is a task "Algebra exam" in subject "Mathematics" due "2027-12-31T23:59" taking 60 minutes

  Scenario: Edit a task's name and description
    When I edit task "Algebra exam" in subject "Mathematics" with:
      | name       | text                     |
      | Final exam | Comprehensive final exam |
    Then I am viewing the task "Final exam" in subject "Mathematics"
    And the task name displayed is "Final exam"
