@wip
Feature: Edit subject
  As an authenticated user
  I want to modify the data of a subject
  So that I can keep it up to date

  Background:
    Given I am logged in
    And I am on the detail page of subject "Mathematics"

  Scenario: Edit name and description
    When I click "Edit"
    And I change the name to "Advanced Mathematics"
    And I change the description to "Calculus III"
    And I click "Save"
    Then the title shows "Advanced Mathematics"
    And the description shows "Calculus III"

  Scenario: Change color
    When I click "Edit"
    And I select color "#c4654a"
    And I click "Save"
    Then the subject color is updated in the detail view and in the grid

  Scenario: Edit is cancelled without saving
    When I click "Edit"
    And I change the name to "Something else"
    And I click "Cancel"
    Then the original subject name is still displayed
