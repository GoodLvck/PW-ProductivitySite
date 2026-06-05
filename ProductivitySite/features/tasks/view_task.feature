Feature: View Task
  In order to manage my task details and subtasks
  As a registered user
  I want to view the details of a task

  Background: There is a registered user with a task
    Given I am logged in as "testuser" with password "TestPass123!"
    And there is a subject named "Mathematics"
    And there is a task "Algebra exam" in subject "Mathematics" due "2027-12-31T23:59" taking 60 minutes

  Scenario: View a task with no subtasks
    When I visit the details page for task "Algebra exam" in subject "Mathematics"
    Then I can see the task name "Algebra exam"
    And there are no subtasks listed

  Scenario: View a task with a subtask
    Given there is a subtask "Review notes" in task "Algebra exam" of subject "Mathematics" due "2027-12-30T23:59" taking 30 minutes
    When I visit the details page for task "Algebra exam" in subject "Mathematics"
    Then I can see the subtask "Review notes"
