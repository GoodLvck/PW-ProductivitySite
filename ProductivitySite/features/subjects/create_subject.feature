Feature: Create Subject
  In order to organise my studies
  As a registered user
  I want to create a new subject

  Background: There is a registered user
    Given I am logged in as "testuser" with password "TestPass123!"

  Scenario: Create a subject with required fields
    When I create a subject with:
      | name        | description                    |
      | Mathematics | Algebra, calculus and geometry |
    Then I am on the subjects page
    And there is 1 subject named "Mathematics"

  Scenario: Cannot create two subjects with the same name
    Given there is a subject named "Physics"
    When I create a subject with:
      | name    | description             |
      | Physics | Another physics subject |
    Then I see an error message "A subject with that name already exists"
