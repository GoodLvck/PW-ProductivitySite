Feature: Delete Subtask
  In order to remove subtasks I no longer need
  As a registered user
  I want to delete a subtask

  Background: There is a registered user with a subtask
    Given I am logged in as "testuser" with password "TestPass123!"
    And there is a subject named "Mathematics"
    And there is a task "Algebra exam" in subject "Mathematics" due "2027-12-31T23:59" taking 120 minutes
    And there is a subtask "Review notes" in task "Algebra exam" of subject "Mathematics" due "2027-12-30T23:59" taking 30 minutes

  Scenario: Delete a subtask
    When I delete subtask "Review notes" in task "Algebra exam" of subject "Mathematics"
    Then I am viewing the task "Algebra exam" in subject "Mathematics"
    And there are no subtasks named "Review notes" in task "Algebra exam"
