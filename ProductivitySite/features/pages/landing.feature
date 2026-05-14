Feature: Public landing page
  As a visitor
  I want to learn about the web application before registering
  So that I can decide whether to sign up

  Background:
    Given I am on "/"

  Scenario: View the landing page
    Then I see the hero section with the main message and CTA
    And I see the features sections (zigzag layout)
    And I see the contact section
    And I see the footer

  Scenario: Go to registration from the navbar
    When I click "Sign Up" in the navbar
    Then I am redirected to "/register"

#  Scenario: Go to registration from the banner
#    When I click "Start now" in the banner
#    Then I am redirected to "/register"

  @wip
  Scenario: Send a contact message
    When I fill in "Name" with "Ana Lopez"
    And I fill in "Email" with "ana@example.com"
    And I fill in "Subject" with "Question about ZenOrbit"
    And I fill in "Message" with "Hello, I would like to know more about the app."
    And I click "Send"
    Then I see the message "Your message has been sent successfully."

  Scenario: Go to login from the navbar
    When I click "Sign in" in the navbar
    Then I am redirected to "/login"

  Scenario: Authenticated user is redirected away from landing
    Given I am already logged in
    When I navigate to "/"
    Then I am redirected to "/dashboard"
