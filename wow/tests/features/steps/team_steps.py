from behave import given, when, then
import requests
import json
from hamcrest import assert_that, equal_to, has_length, greater_than, has_item, has_entries, is_in, anything


# Base URL for the API
BASE_URL = "http://localhost:8001"


@given("the WOW application is running")
def step_impl(context):
    """
    Check if the WOW application is running by making a request to the root endpoint.
    """
    try:
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        context.api_running = True
    except requests.exceptions.ConnectionError:
        context.api_running = False
        assert False, "The WOW application is not running. Please start it before running the tests."


@when("I request all teams")
def step_impl(context):
    """
    Make a request to get all teams.
    """
    response = requests.get(f"{BASE_URL}/teams")
    context.response = response
    context.teams = response.json()


@when('I request the team with ID "{team_id}"')
def step_impl(context, team_id):
    """
    Make a request to get a specific team by ID.
    """
    response = requests.get(f"{BASE_URL}/teams/{team_id}")
    context.response = response
    if response.status_code == 200:
        context.team = response.json()


@when('I request teams with business segment "{business_segment}"')
def step_impl(context, business_segment):
    """
    Make a request to get teams filtered by business segment.
    """
    response = requests.get(f"{BASE_URL}/teams", params={"business_segment": business_segment})
    context.response = response
    context.teams = response.json()
    context.business_segment = business_segment


@when('I request teams with value stream "{value_stream_name}"')
def step_impl(context, value_stream_name):
    """
    Make a request to get teams filtered by value stream.
    """
    response = requests.get(f"{BASE_URL}/teams", params={"value_stream_name": value_stream_name})
    context.response = response
    context.teams = response.json()
    context.value_stream_name = value_stream_name


@then("I should receive a list of teams")
def step_impl(context):
    """
    Check if the response contains a list of teams.
    """
    assert_that(context.teams, has_length(greater_than(0)))


@then("I should receive the team details")
def step_impl(context):
    """
    Check if the response contains team details.
    """
    assert_that(context.team, has_entries({
        "team_id": anything(),
        "team_name": anything(),
        "business_segment": anything(),
        "value_streams": anything(),
        "services_applications": anything(),
        "team_api": anything()
    }))


@then('the team name should be "{team_name}"')
def step_impl(context, team_name):
    """
    Check if the team name matches the expected value.
    """
    assert_that(context.team["team_name"], equal_to(team_name))


@then('all teams should belong to the "{business_segment}" business segment')
def step_impl(context, business_segment):
    """
    Check if all teams belong to the specified business segment.
    """
    for team in context.teams:
        assert_that(team["business_segment"], equal_to(business_segment))


@then('all teams should have the "{value_stream_name}" value stream')
def step_impl(context, value_stream_name):
    """
    Check if all teams have the specified value stream.
    """
    for team in context.teams:
        value_stream_names = [vs["value_stream_name"] for vs in team["value_streams"]]
        assert_that(value_stream_name, is_in(value_stream_names))


@then("the response status code should be {status_code:d}")
def step_impl(context, status_code):
    """
    Check if the response status code matches the expected value.
    """
    assert_that(context.response.status_code, equal_to(status_code))
