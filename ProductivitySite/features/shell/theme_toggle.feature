#@wip
#Feature: Light/dark theme toggle
#  As a user
#  I want to switch between light and dark mode
#  So that I can adapt the interface to my preferences
#
#  Background:
#    Given I am logged in
#    And I am on any page within the DashboardLayout
#
#  Scenario: Activate dark mode
#    Given the app is in light mode
#    When I click the theme button in the header
#    Then the app switches to dark mode
#    And the preference is preserved on page reload
#
#  Scenario: Return to light mode
#    Given the app is in dark mode
#    When I click the theme button
#    Then the app returns to light mode
#
#  Scenario: Theme preference persists across sessions
#    Given I have set the theme to dark mode
#    When I log out and log back in
#    Then the app loads in dark mode
