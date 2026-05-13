Feature: View subjects
  As an authenticated user
  I want to see my subjects and open their detail
  So that I can access their tasks

  Background:
    Given I am logged in

  Scenario: List subjects
    Given I have 3 subjects created
    When I navigate to "/subjects"
    Then I see 3 subject cards in the grid
    And each card shows name, description, and color

  Scenario: Empty state
    Given I have no subjects created
    When I navigate to "/subjects"
    Then I see a message inviting me to create my first subject

  Scenario: Open subject detail
    Given the subject "Mathematics" exists
    When I click on the "Mathematics" card
    Then I see the detail view with its name, description, and task list
    And I see the breadcrumb "Subjects / Mathematics"

  Scenario: Subject card shows task summary
    Given the subject "Mathematics" has 3 pending tasks and 1 completed task
    When I navigate to "/subjects"
    Then the "Mathematics" card shows "3 pending / 1 completed"
