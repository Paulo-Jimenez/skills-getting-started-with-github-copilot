"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Tests follow the AAA (Arrange-Act-Assert) pattern:
  - Arrange: Set up test fixtures and preconditions
  - Act: Execute the action being tested
  - Assert: Verify the expected outcome
"""

import pytest


def test_signup_success(client):
    """
    Test successful signup of a new student for an activity.
    
    Arrange: Prepare a valid activity name and a new email not yet signed up
    Act: Send POST request with activity name and email
    Assert: Verify response status is 200 and student is added to participants
    """
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})
    
    # Assert
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "message" in data, "Response should contain a message"
    assert new_email in data["message"], f"Message should mention {new_email}"
    
    # Verify student was actually added by fetching activities
    verify_response = client.get("/activities")
    activities = verify_response.json()
    assert new_email in activities[activity_name]["participants"], \
        f"{new_email} should be in participants list after signup"


def test_signup_duplicate_email_rejected(client):
    """
    Test that signup fails when student tries to sign up twice for same activity.
    
    Arrange: Choose an activity with existing participants and try to signup with same email
    Act: Send POST request with email already in participants
    Assert: Verify response status is 400 and error message mentions duplicate/already signed up
    """
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"  # Already in Chess Club participants
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})
    
    # Assert
    assert response.status_code == 400, f"Expected 400 for duplicate signup, got {response.status_code}"
    data = response.json()
    assert "detail" in data, "Response should contain error detail"
    assert "already signed up" in data["detail"].lower() or "already" in data["detail"].lower(), \
        "Error message should mention student already signed up"


def test_signup_activity_not_found(client):
    """
    Test that signup fails when activity does not exist.
    
    Arrange: Prepare a non-existent activity name
    Act: Send POST request to signup for non-existent activity
    Assert: Verify response status is 404 and error message mentions activity not found
    """
    # Arrange
    nonexistent_activity = "Quantum Physics Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{nonexistent_activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404, f"Expected 404 for missing activity, got {response.status_code}"
    data = response.json()
    assert "detail" in data, "Response should contain error detail"
    assert "not found" in data["detail"].lower(), \
        "Error message should mention activity not found"


def test_signup_missing_email_parameter(client):
    """
    Test that signup fails when email query parameter is missing.
    
    Arrange: Prepare request without email parameter
    Act: Send POST request without email param
    Assert: Verify response status is 422 (validation error)
    """
    # Arrange
    activity_name = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup")
    
    # Assert
    assert response.status_code == 422, \
        f"Expected 422 for missing email parameter, got {response.status_code}. Response: {response.text}"


def test_signup_beyond_capacity_allowed(client):
    """
    Test that signup currently allows adding participants beyond max_participants.
    
    Arrange: Fill an activity beyond its max_participants limit
    Act: Keep adding participants beyond the max_participants value
    Assert: Verify signups succeed (documenting current behavior)
    
    Note: This test documents the current behavior where capacity is not enforced.
    In the future, capacity validation could be implemented to reject signups 
    when max_participants is reached.
    """
    # Arrange
    # Book Club has max_participants=12 and currently has 2 participants
    activity_name = "Book Club"
    
    # Fill the activity beyond capacity (past 12 participants)
    base_email = "participant_"
    for i in range(15):  # Add 15 more, exceeding the max of 12
        email = f"{base_email}{i}@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        
        # Assert: Current behavior allows signup beyond capacity
        assert response.status_code == 200, \
            f"Current implementation allows signup beyond capacity (iteration {i})"
    
    # Verify all participants were added
    verify_response = client.get("/activities")
    participants = verify_response.json()[activity_name]["participants"]
    assert len(participants) > 12, "Activity has more participants than max_participants"


def test_signup_with_special_characters_in_email(client):
    """
    Test that signup works with valid email addresses containing special characters.
    
    Arrange: Prepare an email with special characters (e.g., with + or .)
    Act: Send POST request with valid email containing special characters
    Assert: Verify response status is 200 and signup succeeds
    """
    # Arrange
    activity_name = "Programming Class"
    email_with_plus = "student+tag@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email_with_plus})
    
    # Assert
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "message" in data, "Response should contain a message"
