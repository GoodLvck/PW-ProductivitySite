Feature: Delete subtask
  As an authenticated user
  I want to delete a subtask
  So that I can remove it from my planning

  Scenario: Confirmed deletion
    Given I am on the subtask detail page
    When I click "Edit"
    And I click "Delete subtask"
    And I confirm
    Then I am returned to the task detail page
    And the subtask no longer appears in the list
    And the subtask counter decreases by 1

  Scenario: Cancel deletion
    When I click "Delete subtask"
    And I cancel the confirmation
    Then the subtask still exists
