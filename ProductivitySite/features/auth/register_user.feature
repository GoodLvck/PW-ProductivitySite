Feature: Register User
  In order to start using ZenOrbit
  As a new visitor
  I want to register a new account

  Scenario: Register with valid credentials
    When I register as user "ana" with email "ana@example.com" and password "AnaPass123!"
    Then there is a registered user with username "ana"
    And I am on the login page

  Scenario: Cannot register with an existing username
    Given exists a user "ana" with password "AnaPass123!"
    When I register as user "ana" with email "other@example.com" and password "AnaPass123!"
    Then there is 1 user with username "ana"
