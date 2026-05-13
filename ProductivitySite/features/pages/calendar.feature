Feature: Calendar
  As an authenticated user
  I want to view my tasks on a calendar
  So that I can plan by due dates

  Background:
    Given I am logged in

  Scenario: Access the calendar
    When I navigate to "/calendar"
    Then I see a calendar with tasks positioned on their due dates

  Scenario: Navigate to the next month
    When I click the next month control
    Then the calendar updates to the corresponding month

  Scenario: Navigate to the previous month
    When I click the previous month control
    Then the calendar updates to the corresponding month

  Scenario: Click a task on the calendar
    When I click a task displayed on the calendar
    Then I am taken to that task's detail page

  Scenario: Days with tasks are visually distinguished
    Given I have tasks due on several dates this month
    Then those days are visually highlighted on the calendar
