Feature: User registration
  As a visitor
  I want to create an account on ZenOrbit
  So that I can access the productivity and study features

  Background:
    Given I am on the "/register" page

  Scenario: Successful registration with valid data
    When I enter "Ana" in the "First name" field
    And I enter "López" in the "Last name" field
    And I enter "ana" in the "Username" field
    And I enter "ana@example.com" in the "Email" field
    And I enter "Secret123!" in the "Password" field
    And I click the "Create account" button
    Then my account is created
    And I am redirected to "/login"

  Scenario: Email already registered
    Given a user with email "ana@example.com" already exists
    When I try to register with that same email
    Then I see the error message "Email is already in use"
    And I remain on "/register"

  Scenario: Weak password
    When I enter a password shorter than 8 characters
    And I click "Create account"
    Then I see the error message "Password must be at least 8 characters"

  Scenario Outline: Required field validation
    When I leave the "<field>" field empty
    And I click "Create account"
    Then I see the message "<message>"

    Examples:
      | field      | message                |
      | First name | First name is required |
      | Last name  | Last name is required  |
      | Username   | Username is required   |
      | Email      | Email is required      |
      | Password   | Password is required   |