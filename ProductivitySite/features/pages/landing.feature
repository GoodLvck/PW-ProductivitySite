Feature: Public landing page
  As a visitor
  I want to learn about ZenOrbit before registering
  So that I can decide whether to sign up

  Background:
    Given I am on "/"

  Scenario: View the landing page
    Then I see the hero section with the main message and CTA
    And I see the features sections (zigzag layout)
    And I see the contact section
    And I see the footer

  Scenario: Go to registration from the landing page
    When I click the "Get started" CTA in the hero
    Then I am redirected to "/register"

  Scenario: Go to login from the navbar
    When I click "Sign in" in the navbar
    Then I am redirected to "/login"

  Scenario: Navbar blur effect on scroll
    When I scroll down
    Then the navbar shows a translucent background with backdrop-blur

  Scenario: Authenticated user is redirected away from landing
    Given I am already logged in
    When I navigate to "/"
    Then I am redirected to "/dashboard"
