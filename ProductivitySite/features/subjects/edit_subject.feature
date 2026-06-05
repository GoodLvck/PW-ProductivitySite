Feature: Edit Subject
  In order to keep my subject information up to date
  As a registered user
  I want to edit an existing subject

  Background: There is a registered user with a subject
    Given I am logged in as "testuser" with password "TestPass123!"
    And there is a subject named "Mathematics"

  Scenario: Edit a subject's name and description
    When I edit subject "Mathematics" with:
      | name           | description                  |
      | Advanced Maths | Advanced algebra and calculus |
    Then I am viewing the subject "Advanced Maths"
    And the subject name displayed is "Advanced Maths"
