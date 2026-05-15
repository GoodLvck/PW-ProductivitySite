Feature: Productivity
  As an authenticated user
  I want to access productivity tools
  So that I can improve my focus and concentration

  Background:
    Given I am logged in

  Scenario: Access the productivity page
    When I navigate to "/productivity"
    Then I see the available tools (timer, focus mode, etc.)

  @wip
  Scenario: Start a focus timer
    When I navigate to "/productivity"
    And I click "Start" on the focus timer
    Then the timer begins counting down
    And I see the remaining time updating in real time

  @wip
  Scenario: Timer completes and notifies the user
    Given a focus timer is running
    When the timer reaches zero
    Then I hear or see a completion notification
    And the timer resets to its default duration
