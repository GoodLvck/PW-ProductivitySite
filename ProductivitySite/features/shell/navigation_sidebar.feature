Feature: Sidebar navigation
  As an authenticated user
  I want to navigate between sections from the sidebar
  So that I can move quickly around the app

  Background:
    Given I am logged in

  Scenario Outline: Navigate to main sections
    When I click "<item>" in the sidebar
    Then I am redirected to "<route>"
    And the "<item>" item is highlighted as active

    Examples:
      | item         | route          |
      | Dashboard    | /dashboard     |
      | Subjects     | /subjects      |
      | Calendar     | /calendar      |
      | Productivity | /productivity  |
      | Profile      | /profile       |

  Scenario: Collapse and expand the sidebar
    When I click the sidebar toggle
    Then the sidebar collapses showing only icons
    When I click it again
    Then the sidebar expands showing icons and labels

  Scenario: Sidebar on mobile
    Given the viewport is mobile
    When I click the sidebar toggle
    Then the sidebar opens as an overlay
    And clicking outside closes it
