Feature: Authorization
  In order to keep my data private
  As a registered user
  I want to ensure other users cannot access my subjects, tasks or subtasks

  Background: Two users, one with data
    Given exists a user "ana" with password "AnaPass123!"
    And I am logged in as "testuser" with password "TestPass123!"
    And there is a subject named "Private Subject"
    And there is a task "Private Task" in subject "Private Subject" due "2027-12-31T23:59" taking 60 minutes
    And there is a subtask "Private Subtask" in task "Private Task" of subject "Private Subject" due "2027-12-30T23:59" taking 30 minutes

  Scenario: User cannot view another user's subject
    Given I am logged in as "ana" with password "AnaPass123!"
    When I try to access the subject "Private Subject" of "testuser"
    Then I see a not found page

  Scenario: User cannot view another user's task
    Given I am logged in as "ana" with password "AnaPass123!"
    When I try to access the task "Private Task" in subject "Private Subject" of "testuser"
    Then I see a not found page

  Scenario: User cannot view another user's subtask
    Given I am logged in as "ana" with password "AnaPass123!"
    When I try to access the subtask "Private Subtask" in task "Private Task" in subject "Private Subject" of "testuser"
    Then I see a not found page
