Feature: Delete Task
  In order to remove tasks I no longer need
  As a registered user
  I want to delete a task

  Background: There is a registered user with a task
    Given I am logged in as "testuser" with password "TestPass123!"
    And there is a subject named "Mathematics"
    And there is a task "Algebra exam" in subject "Mathematics" due "2027-12-31T23:59" taking 60 minutes

  Scenario: Delete a task
    When I delete task "Algebra exam" in subject "Mathematics"
    Then I am viewing the subject "Mathematics"
    And there are no tasks named "Algebra exam" in subject "Mathematics"
