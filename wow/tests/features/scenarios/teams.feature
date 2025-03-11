Feature: Team Information Retrieval
  As an API user
  I want to retrieve information about teams
  So that I can understand team ownership and responsibilities

  Scenario: Retrieve all teams
    Given the WOW application is running
    When I request all teams
    Then I should receive a list of teams
    And the response status code should be 200

  Scenario: Retrieve a specific team by ID
    Given the WOW application is running
    When I request the team with ID "team_alpha"
    Then I should receive the team details
    And the team name should be "Alpha Squad"
    And the response status code should be 200

  Scenario: Filter teams by business segment
    Given the WOW application is running
    When I request teams with business segment "Internet Banking Division"
    Then I should receive a list of teams
    And all teams should belong to the "Internet Banking Division" business segment
    And the response status code should be 200

  Scenario: Filter teams by value stream
    Given the WOW application is running
    When I request teams with value stream "Mortgage Application"
    Then I should receive a list of teams
    And all teams should have the "Mortgage Application" value stream
    And the response status code should be 200

  Scenario: Request a non-existent team
    Given the WOW application is running
    When I request the team with ID "non_existent_team"
    Then the response status code should be 404
