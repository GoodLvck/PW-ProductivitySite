Feature: Edit Subtask
  In order to keep my subtask information up to date
  As a registered user
  I want to edit an existing subtask

  Background: There is a registered user with a subtask
    Given I am logged in as "testuser" with password "TestPass123!"
    And there is a subject named "Mathematics"
    And there is a task "Algebra exam" in subject "Mathematics" due "2027-12-31T23:59" taking 120 minutes
    And there is a subtask "Review notes" in task "Algebra exam" of subject "Mathematics" due "2027-12-30T23:59" taking 30 minutes

  Scenario: Edit a subtask's name and description
    When I edit subtask "Review notes" in task "Algebra exam" of subject "Mathematics" with:
      | name          | description          |
      | Chapter notes | Review each chapter  |
    Then I am viewing the subtask "Chapter notes" in task "Algebra exam" of subject "Mathematics"
    And the subtask name displayed is "Chapter notes"
