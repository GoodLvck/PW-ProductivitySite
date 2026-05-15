Feature: Create subject
  As an authenticated user
  I want to create new subjects
  So that I can organise my study tasks by topic

  Background:
    Given I am logged in
    And I am on "/subjects"

  @wip
  Scenario: Create a subject with valid data
    When I click "New subject"
    And I fill in "Name" with "Mathematics"
    And I fill in "Description" with "Calculus and algebra"
    And I select color "#7d9b76"
    And I click "Create"
    Then the subject "Mathematics" appears in the grid
    And the card uses the selected color

  @wip
  Scenario: Required name validation
    When I click "New subject"
    And I leave the "Name" field empty
    And I click "Create"
    Then the "Create" button remains disabled
    And the subject is not created

  @wip
  Scenario: Cancel creation
    When I click "New subject"
    And I fill in "Name" with "History"
    And I click "Cancel"
    Then the dialog closes
    And the subject "History" does not appear in the grid

  @wip
  Scenario: Subject name must be unique
    Given a subject named "Mathematics" already exists
    When I click "New subject"
    And I fill in "Name" with "Mathematics"
    And I click "Create"
    Then I see the error message "A subject with that name already exists"
