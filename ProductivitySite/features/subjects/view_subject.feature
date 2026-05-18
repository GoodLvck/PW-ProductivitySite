Feature: View Subject
  In order to see my tasks
  As a registered user
  I want to view the details of a subject

  Background: There is a registered user with a subject
    Given I am logged in as "testuser" with password "TestPass123!"
    And there is a subject named "Mathematics"

  Scenario: View a subject with no tasks
    When I visit the details page for subject "Mathematics"
    Then I can see the subject name "Mathematics"
    And there are no tasks listed

  Scenario: View a subject with a pending task
    Given there is a task "Algebra exam" in subject "Mathematics" due "2027-12-31T23:59" taking 60 minutes
    When I visit the details page for subject "Mathematics"
    Then I can see the task "Algebra exam"
