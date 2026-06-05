Feature: Login Validation
  In order to protect user accounts
  As the ZenOrbit system
  I want to reject invalid login attempts

  Scenario: Login with incorrect password
    When I try to login as "testuser" with password "WrongPassword99!"
    Then I see an error message "Please enter a correct username and password"
    And I remain on the login page

  Scenario: Login with a non-existent username
    When I try to login as "nobody_registered" with password "SomePassword1!"
    Then I see an error message "Please enter a correct username and password"
    And I remain on the login page
