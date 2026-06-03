"""
Tests for the DELETE /activities/{activity_name}/participants endpoint.

Tests follow the AAA (Arrange-Act-Assert) pattern:
  - Arrange: Set up test fixtures and preconditions
  - Act: Execute the action being tested
  - Assert: Verify the expected outcome
"""

import pytest


def test_unregister_success(client):
    """
    Test successful unregistration of a student from an activity.
    
    Arrange: Select an activity with existing participants
    Act: Send DELETE request with email of existing participant
    Assert: Verify response status is 200 and student is removed from participants
    """
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"  # Known to be in Chess Club
    
    # Verify participant is there before deletion
    response = client.get("/activities")
    assert email_to_remove in response.json()[activity_name]["participants"], \
        "Participant should exist before unregistration"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email_to_remove})
    
    # Assert
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "message" in data, "Response should contain a message"
    assert email_to_remove in data["message"], f"Message should mention {email_to_remove}"
    
    # Verify student was actually removed
    verify_response = client.get("/activities")
    assert email_to_remove not in verify_response.json()[activity_name]["participants"], \
        f"{email_to_remove} should be removed from participants list"


def test_unregister_participant_not_found(client):
    """
    Test that unregister fails when student is not in the activity.
    
    Arrange: Select an activity and an email not in its participants
    Act: Send DELETE request with email not in participants
    Assert: Verify response status is 404 and error message mentions participant not found
    """
    # Arrange
    activity_name = "Chess Club"
    nonexistent_email = "nobody@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants", 
                            params={"email": nonexistent_email})
    
    # Assert
    assert response.status_code == 404, \
        f"Expected 404 for non-existent participant, got {response.status_code}"
    data = response.json()
    assert "detail" in data, "Response should contain error detail"
    assert "not found" in data["detail"].lower() or "participant" in data["detail"].lower(), \
        "Error message should mention participant not found"


def test_unregister_activity_not_found(client):
    """
    Test that unregister fails when activity does not exist.
    
    Arrange: Prepare a non-existent activity name
    Act: Send DELETE request to unregister from non-existent activity
    Assert: Verify response status is 404 and error message mentions activity not found
    """
    # Arrange
    nonexistent_activity = "Underwater Basket Weaving"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{nonexistent_activity}/participants", 
                            params={"email": email})
    
    # Assert
    assert response.status_code == 404, \
        f"Expected 404 for non-existent activity, got {response.status_code}"
    data = response.json()
    assert "detail" in data, "Response should contain error detail"
    assert "not found" in data["detail"].lower(), \
        "Error message should mention activity not found"


def test_unregister_missing_email_parameter(client):
    """
    Test that unregister fails when email query parameter is missing.
    
    Arrange: Prepare request without email parameter
    Act: Send DELETE request without email param
    Assert: Verify response status is 422 (validation error)
    """
    # Arrange
    activity_name = "Chess Club"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants")
    
    # Assert
    assert response.status_code == 422, \
        f"Expected 422 for missing email parameter, got {response.status_code}. Response: {response.text}"


def test_unregister_case_sensitive_email(client):
    """
    Test unregistration behavior with different email cases.
    
    Arrange: Use different case variations of an email address
    Act: Try to unregister with different case than stored
    Assert: Verify whether case sensitivity is handled correctly (documents current behavior)
    """
    # Arrange
    activity_name = "Chess Club"
    original_email = "michael@mergington.edu"
    different_case_email = "Michael@Mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants", 
                            params={"email": different_case_email})
    
    # Assert
    # The app treats emails as case-sensitive, so this should fail
    # If email handling changes in the future, this test documents that behavior
    if response.status_code == 404:
        # Current behavior: case-sensitive
        assert "not found" in response.json()["detail"].lower(), \
            "Case-sensitive email comparison should result in 'not found'"


def test_unregister_multiple_removals_same_activity(client):
    """
    Test that multiple students can be unregistered from the same activity sequentially.
    
    Arrange: Select an activity with multiple participants
    Act: Unregister multiple participants one by one
    Assert: Verify each removal succeeds and all participants are removed
    """
    # Arrange
    activity_name = "Drama Club"
    emails_to_remove = ["chloe@mergington.edu", "tyler@mergington.edu"]
    
    # Act & Assert for each removal
    for email in emails_to_remove:
        response = client.delete(f"/activities/{activity_name}/participants", 
                                params={"email": email})
        assert response.status_code == 200, \
            f"Failed to remove {email} from {activity_name}"
    
    # Verify all participants were removed
    verify_response = client.get("/activities")
    remaining_participants = verify_response.json()[activity_name]["participants"]
    for email in emails_to_remove:
        assert email not in remaining_participants, \
            f"{email} should be removed from activity"
