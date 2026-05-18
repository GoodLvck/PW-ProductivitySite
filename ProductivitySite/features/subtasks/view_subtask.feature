Feature: View Subtask
  In order to manage my subtask details
  As a registered user
  I want to view the details of a subtask

  Background: There is a registered user with a subtask
    Given I am logged in as "testuser" with password "TestPass123!"
    And there is a subject named "Mathematics"
    And there is a task "Algebra exam" in subject "Mathematics" due "2027-12-31T23:59" taking 120 minutes
    And there is a subtask "Review notes" in task "Algebra exam" of subject "Mathematics" due "2027-12-30T23:59" taking 30 minutes

  Scenario: View a subtask's details
    When I visit the details page for subtask "Review notes" in task "Algebra exam" of subject "Mathematics"
    Then I can see the subtask name "Review notes"
    And I can see the task it belongs to "Algebra exam"
    And I can see the subject it belongs to "Mathematics"
