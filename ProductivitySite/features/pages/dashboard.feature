Feature: Dashboard
  As an authenticated user
  I want to see an overview of my activity
  So that I have quick context when I open the app

  Background:
    Given I am logged in

  @wip
  Scenario: View the dashboard after logging in
    When I navigate to "/dashboard"
    Then I see summary cards with statistics (subjects, tasks, progress)
    And I see a personalised greeting

#  @wip
#  Scenario: Dashboard reflects up-to-date data
#    Given I have just completed a task
#    When I navigate to "/dashboard"
#    Then the statistics reflect the updated progress

#  @wip
#  Scenario: Dashboard shows upcoming due dates
#    Given I have tasks due within the next 7 days
#    When I navigate to "/dashboard"
#    Then I see an "Upcoming" section listing those tasks
