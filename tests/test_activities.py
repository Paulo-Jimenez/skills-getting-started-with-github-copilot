"""
Tests for the GET /activities and GET / endpoints.

Tests follow the AAA (Arrange-Act-Assert) pattern:
  - Arrange: Set up test fixtures and preconditions
  - Act: Execute the action being tested
  - Assert: Verify the expected outcome
"""

import pytest


def test_get_activities_success(client):
    """
    Test that GET /activities returns all activities with correct structure.
    
    Arrange: Create a test client with fresh activities database
    Act: Send GET request to /activities endpoint
    Assert: Verify response status is 200 and contains all 9 activities with required fields
    """
    # Arrange
    expected_activity_count = 9
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    
    assert len(activities) == expected_activity_count, "Should return all 9 activities"
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str), f"Activity name should be string, got {type(activity_name)}"
        assert isinstance(activity_data, dict), f"Activity data should be dict, got {type(activity_data)}"
        assert required_fields.issubset(activity_data.keys()), \
            f"Activity '{activity_name}' missing required fields. Got: {activity_data.keys()}"
        assert isinstance(activity_data["participants"], list), \
            f"Participants should be a list, got {type(activity_data['participants'])}"


def test_get_root_redirects_to_static(client):
    """
    Test that GET / redirects to the static index.html page.
    
    Arrange: Create a test client
    Act: Send GET request to root endpoint
    Assert: Verify response is a redirect to /static/index.html
    """
    # Arrange
    expected_redirect_url = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307, "Should return redirect status code"
    assert "location" in response.headers.keys() or "Location" in response.headers.keys(), \
        "Response should include location header for redirect"
    
    # Check redirect location (could be in different case)
    location = response.headers.get("location") or response.headers.get("Location")
    assert location == expected_redirect_url, \
        f"Should redirect to {expected_redirect_url}, got {location}"
